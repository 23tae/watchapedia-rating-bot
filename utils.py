rating_classes_filename = './data/rating_classes.txt'
rating_words_filename = './data/rating_words.txt'
movie_urls_filename = "./movie_urls.txt"


def get_target_class_name(rating: str) -> str:
    class_name_file = open(rating_classes_filename, 'r')
    class_names = class_name_file.readlines()
    converted_rating = int(float(rating) * 2)
    class_name = class_names[converted_rating - 1].rstrip('\n')
    return class_name


def get_current_class_name(word: str) -> str:
    with open(rating_classes_filename, 'r') as file:
        classes = file.readlines()
    with open(rating_words_filename, 'r') as file:
        words = file.readlines()
    for w in words:
        if word in w:
            return classes[words.index(w)].rstrip('\n')
