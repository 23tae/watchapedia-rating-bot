import os


def get_content_index(initial: str) -> int:
    if initial == 'm':
        return 1
    elif initial == 't':
        return 2
    elif initial == 'b':
        return 3
    elif initial == 'w':
        return 4
    return None


def get_content_name(idx: int) -> str:
    if idx == 1:
        content_name = 'movies'
    elif idx == 2:
        content_name = 'tv_seasons'
    elif idx == 3:
        content_name = 'books'
    elif idx == 4:
        content_name = 'webtoons'
    else:
        content_name = None
    return content_name


def get_url_output_filename(idx: int) -> str:
    content_name = get_content_name(idx)
    return os.path.join('./result', f'{content_name}_urls.txt')


def get_rating_index(rating: str) -> int:
    return 11 - int(float(rating) * 2)


def get_rating_page(profile_url: str, idx: int) -> str:
    content_name = get_content_name(idx)
    rating_page_url = os.path.join(
        profile_url, f'contents/{content_name}/ratings')
    return rating_page_url
