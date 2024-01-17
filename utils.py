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


def get_url_output_filename(idx: int) -> str:
    if idx == 1:
        filename = 'movie_urls.txt'
    elif idx == 2:
        filename = 'tv_program_urls.txt'
    elif idx == 3:
        filename = 'book_urls.txt'
    elif idx == 4:
        filename = 'webtoon_urls.txt'
    return os.path.join('./result', filename)
