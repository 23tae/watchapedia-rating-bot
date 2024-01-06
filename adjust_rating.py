from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import ssl
import os


def run_webdriver(my_account: dict):
    driver = set_options()
    move_main_page(my_account, driver)
    move_rating_page(driver)

    # driver.quit()


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
    return driver


def move_main_page(my_account: dict, driver: webdriver):
    # 페이지 이동
    driver.get("https://pedia.watcha.com/ko-KR/")
    # 왓챠피디아 로그인

    # 로그인 버튼이 클릭 가능할 때까지 대기
    wait = WebDriverWait(driver, 10)

    # div가 존재하는지 확인
    try:
        intercepting_div = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')))

        # div가 존재하면 닫기 클릭
        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()
    except:
        # div가 존재하지 않는 경우
        pass

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div[1]/header[1]/nav/div/div/ul/li[7]/button')))

    login_button.click()

    driver.implicitly_wait(10)
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    login_id.send_keys(my_account['username'])
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(my_account['password'])
    login_id.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)


def move_rating_page(driver: webdriver):
    wait = WebDriverWait(driver, 10)
    try:
        intercepting_div = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.css-1bbirrh.e1npj76i6')))

        close_button = driver.find_element(
            By.CSS_SELECTOR, 'span.css-69ff8n.e1npj76i0')
        close_button.click()
    except:
        pass

    # 프로필 버튼 클릭
    profile_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div[1]/header[1]/nav/div/div/ul/li[9]/a/div/div')))
    profile_button.click()

    # 평가 페이지 클릭
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/section/div/div/div/section[1]/div/div[3]/a[1]/span[2]').click()

    # 영화 페이지 클릭
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/section/div/ul/li[1]/div/div[1]').click()
