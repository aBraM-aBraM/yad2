import undetected_chromedriver
import logging

import consts
import predicates
from yad2 import Yad2


def initialize_driver():
    options = undetected_chromedriver.ChromeOptions()

    # setting profile
    options.user_data_dir = consts.PROFILE_PATH

    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    driver = undetected_chromedriver.Chrome(options=options)
    driver.implicitly_wait(10)

    return driver


def main():
    try:
        driver = initialize_driver()
        logging.basicConfig(filename="result.log")
        yad2 = Yad2(driver, consts.ELECTRIC_GUITARS_URL)
        products = yad2.get_predicated_products(predicates.is_fender)
        map(logging.info, products)
        driver.close()
    except Exception as e:
        logging.critical(e)


if __name__ == '__main__':
    main()
