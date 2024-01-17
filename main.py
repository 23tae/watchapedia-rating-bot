import user_info
import adjust_rating
import check_validity

import sys


def main(arg: str):
    content_idx, rating, limit, is_save_url = check_validity.check(arg)
    my_account = user_info.get_account()
    adjust_rating.run_webdriver(
        my_account, content_idx, rating, limit, is_save_url)


if __name__ == '__main__':
    main(sys.argv)
