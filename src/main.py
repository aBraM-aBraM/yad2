import traceback
from _datetime import datetime
import json
import os
from typing import List

import undetected_chromedriver
import logging

import consts
import predicates
from structs import Details
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


def save_products(products: List[Details]):
    os.makedirs(consts.PRODUCTS_DIR, exist_ok=True)
    product_path = os.path.join(consts.PRODUCTS_DIR, datetime.now().strftime("%d_%m_%Y__%H_%M_%S_product"))
    with open(product_path, "w") as products_fd:
        products_fd.write(json.dumps([product.__dict__ for product in products]))


def main():
    try:
        driver = initialize_driver()
        logging.basicConfig(filename="../yad2.log",
                            filemode="w",
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            level=logging.INFO,
                            datefmt="%Y-%m-%d %H:%M:%S")

        yad2 = Yad2(driver, consts.ELECTRIC_GUITARS_URL)

        products = yad2.get_predicated_products(predicates.contains_tokens(consts.FENDER_TOKENS),
                                                predicates.max_price(7000),
                                                predicates.min_price(4000))

        save_products(products)

        driver.close()
    except Exception as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())


if __name__ == '__main__':
    main()
