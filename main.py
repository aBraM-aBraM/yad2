import undetected_chromedriver

import consts
from yad2 import Yad2


def initialize_driver():
    options = undetected_chromedriver.ChromeOptions()

    # setting profile
    options.user_data_dir = "c:\\temp\\profile"

    # another way to set profile is the below (which takes precedence if both variants are used
    options.add_argument('--user-data-dir=D:\\temp\\profile3 ')

    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = undetected_chromedriver.Chrome(options=options)

    return driver


def main():
    driver = initialize_driver()
    yad2 = Yad2(driver)
    yad2.get_predicated_products(consts.ELECTRIC_GUITARS_URL, None)


if __name__ == '__main__':
    main()
