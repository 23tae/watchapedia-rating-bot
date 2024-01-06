import user_info
import adjust_rating
import check_validity

import sys

file_path = './data/users.txt'


def main(arg: str):
    if check_validity.is_arg_valid(arg) == False:
        print('Usage: python3 main.py <rating>\n(rating: 0.5 ~ 5.0 (0.5단위))')
        return
    my_account = user_info.get_account()
    adjust_rating.run_webdriver(my_account)


if __name__ == '__main__':
    main(sys.argv)
