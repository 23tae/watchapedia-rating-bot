def get_content_value(str) -> str:
    if str == 'm':
        return '영화'
    elif str == 't':
        return 'TV 프로그램'
    elif str == 'b':
        return '책'
    elif str == 'w':
        return '웹툰'
    return None


def get_content_index(str) -> int:
    if str == 'm':
        return 1
    elif str == 't':
        return 2
    elif str == 'b':
        return 3
    elif str == 'w':
        return 4
    return None
