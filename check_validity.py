import os


def is_arg_valid(arg: str) -> bool:
    if len(arg) != 2:
        return False
    rating = arg[1]
    arg_len = len(rating)
    if arg_len == 1:
        if rating >= '1' and rating <= '5':
            return True
    elif arg_len == 3 and rating[1] == '.':
        if rating[2] == '0':
            if rating[0] >= '1' and rating[0] <= '5':
                return True
        elif rating[2] == '5':
            if rating[0] >= '0' and rating[0] <= '4':
                return True
    return False


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
