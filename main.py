import user_info
import adjust_rating
import check_validity

import sys


def main(arg: str):
    rating = check_validity.get_rating(arg)
    my_account = user_info.get_account()
    adjust_rating.run_webdriver(my_account, rating)


if __name__ == '__main__':
    main(sys.argv)
