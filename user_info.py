from dotenv import load_dotenv
import os


def get_account() -> dict:
    load_dotenv()
    username = os.getenv('WATCHA_USERNAME')
    password = os.getenv('WATCHA_PASSWORD')
    return ({'username': username, 'password': password})
