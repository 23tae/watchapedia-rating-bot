import utils

import os

content_url_output_file = ""  # 별점 조정할 영화의 url을 저장할 파일
default_limit = 50


def check(arg: str) -> tuple[int, str, int, bool]:
    global content_url_output_file

    content_idx, rating, limit = check_argument(arg)
    content_url_output_file = utils.get_url_output_filename(content_idx)
    is_save_url = delete_previous_file(content_url_output_file)
    return content_idx, rating, limit, is_save_url


def check_argument(arg: str) -> tuple[int, str, int]:
    error_msg = 'Usage: python3 main.py <type> <rating> <limit>\n(type: m(영화), t(TV 프로그램), b(책), w(웹툰)\trating: 0.5~5.0(0.5단위))\tlimit: 1~50\n'
    if len(arg) < 3 or arg[1] not in ['m', 't', 'b', 'w']:
        print(error_msg)
        raise Exception()
    content_idx = utils.get_content_index(arg[1])
    rating = get_rating(arg[2])
    if rating is None:
        print(error_msg)
        raise Exception()
    if len(arg) == 3:
        limit = default_limit
    else:
        limit = int(arg[3])
        if limit <= 0 or limit > default_limit:
            print(error_msg)
            raise Exception()
    return content_idx, rating, limit


def get_rating(rating: str) -> str | None:
    arg_len = len(rating)
    if arg_len == 1:
        if '1' <= rating <= '5':
            return rating + '.0'
    elif arg_len == 3 and rating[1] == '.':
        if rating[2] == '0':
            if '1' <= rating[0] <= '5':
                return rating
        elif rating[2] == '5':
            if '0' <= rating[0] <= '4':
                return rating
    return None


def delete_previous_file(file_path) -> bool:
    try:
        if os.path.exists(file_path):
            user_input = input(
                f"파일 {file_path}이(가) 존재합니다. 다시 생성하시겠습니까? (y/N): ").lower()

            if user_input == 'y':
                os.remove(file_path)
                print(f"파일 {file_path}이(가) 삭제되었습니다.")
                return True
            else:
                print("삭제를 취소했습니다.")
                return False
        else:
            create_dir_if_not_exists(file_path)
            return True
    except Exception as e:
        print(f"Error: {e}")


def create_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
