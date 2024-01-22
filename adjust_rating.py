import check_validity
import utils

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import ssl
import time
from stopwatch import Stopwatch
import urllib.parse


def run_webdriver(my_account: dict, content_idx: int, rating: str, limit: int, is_save_url: bool, t: Stopwatch):
    driver = set_options()
    if move_main_page(my_account, driver) is False:
        driver.quit()
        return
    if is_save_url:
        page_url = get_rating_page(driver, content_idx)
        save_content_urls(driver, rating, limit, page_url, t)
    adjust_rating(driver, rating, limit, t)
    driver.quit()


def set_options():
    ssl._create_default_https_context = ssl._create_unverified_context
    # 브라우저 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    # chrome_options.add_argument('--headless=new')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('incognito')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# 1. 왓챠피디아 로그인
# 왓챠피디아 메인 페이지로 이동
def move_main_page(my_account: dict, driver: webdriver) -> bool:
    # 페이지 이동
    driver.get("https://pedia.watcha.com/ko-KR/")

    wait = WebDriverWait(driver, 3)

    # div가 존재하면 닫기 버튼 클릭
    intercepting_div = driver.find_elements(
        By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')
    if len(intercepting_div) > 0:
        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()

    login_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button.css-jt7ti-StylelessButton-LoginButton')))

    login_button.click()

    # 왓챠피디아 로그인
    print("1. 왓챠피디아 로그인: ", end='', flush=True)
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    login_id.send_keys(my_account['username'])
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(my_account['password'])
    login_id.send_keys(Keys.ENTER)

    # 로그인 성공 여부 확인
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-11row1x.e1cn7arl4')))
    except:
        print("성공")
        return True

    print("실패")
    return False


# 별점 보관함 url 반환
def get_rating_page(driver: webdriver, content_idx: int) -> str:
    profile_button = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/header[1]/nav/div/div/ul/li[9]/a')
    profile_url = profile_button.get_attribute('href')
    rating_page_url = utils.get_rating_page(profile_url, content_idx)
    driver.implicitly_wait(3)
    return rating_page_url


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_to_right(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'start' });", element)


# 2. 콘텐츠 정보 저장
# 변경할 별점을 가진 콘텐츠의 url을 파일에 저장
def save_content_urls(driver: webdriver, rating: str, limit: int, page_url: str, t: Stopwatch):

    print("2. 콘텐츠 정보 저장")
    t.tick()
    count = 0
    wait = WebDriverWait(driver, 2)
    rating_idx = utils.get_rating_index(rating)
    with open(check_validity.content_url_output_file, 'a') as file:
        for i in range(1, 11):  # 점수별 콘텐츠
            if i == rating_idx:
                continue
            current_rating_idx = 11 - i
            current_rating_page_url = urllib.parse.urljoin(
                page_url, str(current_rating_idx))
            driver.get(current_rating_page_url)
            try:
                driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[1]/section/section/div[1]/div/div/section/div/div')
                continue
            except NoSuchElementException:
                pass
            j = 1
            while True:
                try:
                    xpath = f'//*[@id="root"]/div/div[1]/section/section/div[1]/div/div/ul/li[{j}]/a'
                    j += 1
                    url_element = wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath)))
                    content_url = url_element.get_attribute('href')
                    file.write(content_url + '\n')
                    count += 1
                except TimeoutException:
                    break
                if count >= limit:
                    return
                scroll_to_bottom(driver)
        scroll_to_bottom(driver)

    print(f"콘텐츠 정보 저장 완료. 소요시간: {t.tick('콘텐츠 정보 저장'):.2f}s")


# 3. 별점 조정
def adjust_rating(driver: webdriver, target_rating: str, limit: int, t: Stopwatch):

    print("3. 별점 조정")
    t2 = Stopwatch()
    t.tick()
    t2.start()
    repetition_limit = 5

    with open(check_validity.content_url_output_file, 'r') as file:
        content_urls = file.readlines()

    try:
        for content_url, i in zip(content_urls, range(1, len(content_urls) + 1)):
            driver.get(content_url)
            wait = WebDriverWait(driver, 5)

            # 페이지가 완전히 로드될 때까지 대기
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'section.css-19lmqd7.edz00v813')
            ))

            # 목표 별점 클릭
            modified_target_rating = int(float(target_rating) * 2)
            star_box = driver.find_element(By.CSS_SELECTOR, 'div.e10lmt5b3')
            size = star_box.size
            ac = ActionChains(driver)
            ac.move_to_element_with_offset(
                star_box, (size.get('width') / 10) * (modified_target_rating - 5.5), 0).click()
            ac.perform()

            if i >= limit:
                break

            # 일정 시간 대기
            if i % repetition_limit == 0:
                print(
                    f"{repetition_limit}개 조정 완료(현재 {i}번). 소요시간: {t2.tick():.2f}s")
                print("대기중...", end='\r', flush=True)
                time.sleep(repetition_limit)
                t2.tick()
                print("조정 재개", end='\r', flush=True)
            continue

    except TimeoutException as e:
        print(f'{i}번({content_url}) 시간초과. 소요시간: {t.tick("별점 조정"):.2f}s')
        print(e)
        return

    print(f"별점 조정 완료. 소요시간: {t.tick('별점 조정'):.2f}s")
