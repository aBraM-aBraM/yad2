import undetected_chromedriver

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

    return driver


def main():
    driver = initialize_driver()
    yad2 = Yad2(driver)
    products = yad2.get_predicated_products(consts.ELECTRIC_GUITARS_URL, predicates.is_fender)
    for products in products:
        print("===========")
        print(f"name: {products.details.title}")
        print(f"price: {products.details.price}")
        print(f"phone number: {products.phone}")
        print("===========")


if __name__ == '__main__':
    main()
