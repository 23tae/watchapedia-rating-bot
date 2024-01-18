import user_info
import adjust_rating
import check_validity

import sys
from stopwatch import Stopwatch


def main(arg: str):
    t = Stopwatch()
    t.start()
    content_idx, rating, limit, is_save_url = check_validity.check(arg)
    my_account = user_info.get_account()
    adjust_rating.run_webdriver(
        my_account, content_idx, rating, limit, is_save_url, t)
    t.stop()
    print(f"전체 실행시간: {t.time_total:.2f}s")


if __name__ == '__main__':
    main(sys.argv)
