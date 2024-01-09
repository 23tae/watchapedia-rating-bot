import os


def get_rating(arg: str) -> str:
    if len(arg) == 2:
        rating = arg[1]
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
    print('Usage: python3 main.py <rating>\n(rating: 0.5 ~ 5.0 (0.5단위))')
    raise Exception()


def delete_previous_file(file_path) -> bool:
    try:
        if os.path.exists(file_path):
            user_input = input(
                f"파일 {file_path}이(가) 존재합니다. 삭제하시겠습니까? (y/N): ").lower()

            if user_input == 'y':
                os.remove(file_path)
                print(f"파일 {file_path}이(가) 삭제되었습니다.")
                return True
            else:
                print("삭제를 취소했습니다.")
                return False
        else:
            return True
    except Exception as e:
        print(f"Error: {e}")

def create_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)