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


def run_webdriver(my_account: dict, rating: str):
    driver = set_options()
    move_main_page(my_account, driver)
    total_movies = move_rating_page(driver)
    if save_movie_urls(driver, total_movies, rating) is True:
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
    driver.implicitly_wait(5)
    return driver


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
        (By.XPATH, '//*[@id="root"]/div/div[1]/header[1]/nav/div/div/ul/li[7]/button')))

    login_button.click()

    # 왓챠피디아 로그인
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    login_id.send_keys(my_account['username'])
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(my_account['password'])
    login_id.send_keys(Keys.ENTER)


def move_rating_page(driver: webdriver) -> int:
    wait = WebDriverWait(driver, 5)

    intercepting_div = driver.find_elements(
        By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')

    if len(intercepting_div) > 0:
        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()

    # 프로필 버튼 클릭
    profile_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div[1]/header[1]/nav/div/div/ul/li[9]/a/div/div')))
    profile_button.click()

    # 평가 페이지 클릭
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/section/div/div/div/section[1]/div/div[3]/a[1]/span[2]').click()

    # 평가한 영화 개수 확인
    value_span = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="root"]/div/div[1]/section/div/ul/li[1]/div/div[1]/a/h2/span')))
    value = value_span.text
    total_movies = int(value)

    # 영화 페이지 클릭
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/section/div/ul/li[1]/div/div[1]').click()

    return total_movies


def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def save_movie_urls(driver: webdriver, total_movies: int, rating: str) -> bool:

    output_file = utils.movie_urls_filename  # 별점 조정할 영화의 url을 저장할 파일
    skip_value = '평가함 ★ ' + rating  # 별점을 유지할 영화의 값

    if check_validity.delete_previous_file(output_file) is False:
        return True
    check_validity.create_dir_if_not_exists(output_file)
    try:
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
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def adjust_rating(driver: webdriver, rating: str):

    target_rating_class = utils.get_target_class_name(rating)

    with open(utils.movie_urls_filename, 'r') as file:
        movie_urls = file.readlines()

    for movie_url in movie_urls:
        driver.get(movie_url)
        wait = WebDriverWait(driver, 5)

        # 페이지가 완전히 로드될 때까지 대기
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[1]/section/div/div[2]/div/div[1]/div/div[2]/section[1]/div[2]/section[2]/div/section')
        ))

        rating_word = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[1]/section/div/div[2]/div/div[1]/div/div[2]/section[1]/div[2]/section[1]/div[1]/div[2]/div')
        )).text
        current_star_class = utils.get_current_class_name(rating_word)
        print(current_star_class)
        continue
        # 해당 별점이 클릭 가능할 때까지 대기한 후 클릭
        star_xpath = f'//div[@class="{target_rating_class}"]'
        star_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, star_xpath)))
        star_element.click()
