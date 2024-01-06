import user_info
import adjust_rating

file_path = './data/users.txt'


def main():
    my_account = user_info.get_account()
    adjust_rating.run_webdriver(my_account)


if __name__ == '__main__':
    main()
