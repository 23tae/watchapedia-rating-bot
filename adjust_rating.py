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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import ssl
import time


def run_webdriver(my_account: dict, content_idx: int, rating: str, is_save_url: bool):
    driver = set_options()
    if move_main_page(my_account, driver) is False:
        driver.quit()
        return
    if is_save_url:
        total_contents = move_rating_page(driver, content_idx)
        save_content_urls(driver, total_contents, rating)
    adjust_rating(driver, rating)
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
    # driver.implicitly_wait(2)
    return driver


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
        print("로그인 성공")
        return True

    print("로그인 실패")
    return False


# 콘텐츠 평점 페이지로 이동
def move_rating_page(driver: webdriver, content_idx: int) -> int:

    wait = WebDriverWait(driver, 5)

    intercepting_div = driver.find_elements(
        By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')

    if len(intercepting_div) > 0:
        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()

    # 프로필 버튼 클릭
    partial_profile_class_name = "ProfilePhotoImage-ProfilePhotoImage"

    profile_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f'div[class*="{partial_profile_class_name}"]')))
    profile_button.click()

    # 평가 페이지 클릭
    wait.until(EC.presence_of_element_located(
        (By.XPATH,
         '//*[@id="root"]/div/div[1]/section/div/div/div/section[1]/div/div[3]/a[1]')
    )).click()

    # 평가한 콘텐츠 개수 확인
    value_span = wait.until(EC.presence_of_element_located(
        (By.XPATH, f'//*[@id="root"]/div/div[1]/section/div/ul/li[{content_idx}]/div/div[1]/a/h2/span')))
    value = value_span.text
    total_contents = int(value)

    # 콘텐츠 페이지 클릭
    value_span.click()

    return total_contents


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# 변경할 별점을 가진 콘텐츠의 url을 파일에 저장
def save_content_urls(driver: webdriver, total_contents: int, rating: str):

    skip_value = '평가함 ★ ' + rating  # 별점을 유지할 콘텐츠의 값

    print("콘텐츠 정보 저장 시작")

    with open(check_validity.content_url_output_file, 'a') as file:
        for i in range(1, total_contents + 1):
            xpath = f'//*[@id="root"]/div/div[1]/section/section/div[1]/section/div[1]/div/ul/li[{i}]/a/div[2]/div[2]'
            try:
                rating_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                rating_text = rating_element.text
                content_url_element = driver.find_element(
                    By.XPATH, f'//*[@id="root"]/div/div[1]/section/section/div[1]/section/div[1]/div/ul/li[{i}]/a')
                content_url = content_url_element.get_attribute('href')
                if skip_value not in rating_text:
                    file.write(content_url + '\n')
                i += 1
            except StaleElementReferenceException:
                continue

            scroll_to_bottom(driver)

    print("콘텐츠 정보 저장 완료")


# 별점 조정
def adjust_rating(driver: webdriver, target_rating: str):

    print("별점 조정 시작")

    with open(check_validity.content_url_output_file, 'r') as file:
        content_urls = file.readlines()

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

        # 일정 시간 대기
        if i % 50 == 0:
            print(f"콘텐츠 {i}개 평점 조정 완료")
            time.sleep(5)

    print("별점 조정 완료")
