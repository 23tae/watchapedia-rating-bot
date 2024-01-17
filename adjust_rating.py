import check_validity
import utils

from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request
import ssl
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

output_file = utils.movie_urls_filename  # 별점 조정할 영화의 url을 저장할 파일


def run_webdriver(my_account: dict, rating: str):
    driver = set_options()
    move_main_page(my_account, driver)
    total_movies = move_rating_page(driver)
    if total_movies != -1:
        save_movie_urls(driver, total_movies, rating)
    adjust_rating(driver, rating)
    driver.quit()


def set_options():
    ssl._create_default_https_context = ssl._create_unverified_context
    # 브라우저 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    chrome_options.add_argument('incognito')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(2)
    return driver


# 왓챠피디아 메인 페이지로 이동
def move_main_page(my_account: dict, driver: webdriver):
    # 페이지 이동
    driver.get("https://pedia.watcha.com/ko-KR/")

    wait = WebDriverWait(driver, 5)

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


# 평가한 영화 페이지로 이동
def move_rating_page(driver: webdriver) -> int:
    global output_file

    if check_validity.delete_previous_file(output_file) is False:
        return -1
    check_validity.create_dir_if_not_exists(output_file)

    wait = WebDriverWait(driver, 5)

    intercepting_div = driver.find_elements(
        By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')

    if len(intercepting_div) > 0:
        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()

    # 프로필 버튼 클릭
    profile_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div.css-17jpe4g-ProfilePhotoImage-ProfilePhotoImage')))
    profile_button.click()

    # 평가 페이지 클릭
    driver.find_element(
        By.CSS_SELECTOR, 'a.e6k12944.css-1kn1ani.eovgsd00').click()

    # 평가한 영화 개수 확인
    value_span = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'span.css-rh8g4g.eozj6dy1')))
    value = value_span.text
    total_movies = int(value)

    # 영화 페이지 클릭
    driver.find_element(
        By.CSS_SELECTOR, 'h2.css-ksan24.eozj6dy2').click()

    return total_movies


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# 변경할 별점을 가진 영화의 url을 파일에 저장
def save_movie_urls(driver: webdriver, total_movies: int, rating: str):

    global output_file
    skip_value = '평가함 ★ ' + rating  # 별점을 유지할 영화의 값

    with open(output_file, 'a') as file:
        for i in range(1, total_movies + 1):
            xpath = f'//*[@id="root"]/div/div[1]/section/section/div[1]/section/div[1]/div/ul/li[{i}]/a/div[2]/div[2]'
            try:
                rating_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                rating_text = rating_element.text
                movie_url_element = driver.find_element(
                    By.XPATH, f'//*[@id="root"]/div/div[1]/section/section/div[1]/section/div[1]/div/ul/li[{i}]/a')
                movie_url = movie_url_element.get_attribute('href')
                if skip_value not in rating_text:
                    file.write(movie_url + '\n')
                i += 1

            except StaleElementReferenceException:
                continue

            scroll_to_bottom(driver)


# 별점 조정
def adjust_rating(driver: webdriver, target_rating: str):

    with open(utils.movie_urls_filename, 'r') as file:
        movie_urls = file.readlines()

    for movie_url in movie_urls:
        driver.get(movie_url)
        wait = WebDriverWait(driver, 5)

        # 페이지가 완전히 로드될 때까지 대기
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'section.css-19lmqd7.edz00v813')
        ))

        rating_word = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.e10lmt5b1 > div.e1iiuhl30')
        )).text
        modified_target_rating = int(float(target_rating) * 2)
        star_box = driver.find_element(By.CSS_SELECTOR, 'div.e10lmt5b3')
        size = star_box.size
        ac = ActionChains(driver)
        ac.move_to_element_with_offset(
            star_box, (size.get('width') / 10) * (modified_target_rating - 5.5), 0).click()
        ac.perform()
