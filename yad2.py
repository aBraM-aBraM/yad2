from typing import List

import utils

from selenium.webdriver.common.by import By
import re

from undetected_chromedriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from structs import Details, Product


class Yad2:
    YAD2_ITEM_PATTERN = re.compile(r"^feed_item_\d+\b")  # item id regex

    def __init__(self, driver):
        self._driver = driver

    def _get_web_elements(self, url) -> List[WebElement]:
        self._driver.get(url)

        return [web_element for web_element in
                self._driver.find_element(By.CLASS_NAME, "feed_list").find_elements(By.CSS_SELECTOR, "*")
                if Yad2.YAD2_ITEM_PATTERN.match(web_element.get_attribute("id"))]

    def _get_phone_number(self, web_element: WebElement) -> str:
        image_element: WebElement = web_element.find_element(By.XPATH, './child::div[starts-with(@id, "image_")]')
        image_element.click()
        phone_button: WebElement = utils.retry(self._driver.find_element, By.CLASS_NAME,
                                               'lightbox_contact_seller_button',
                                               exceptions=(NoSuchElementException,),
                                               timeout=0.1)
        phone_button.click()
        phone_number_element: WebElement = utils.retry(self._driver.find_element, By.XPATH,
                                                       '//a[starts-with(@class, "phone_number")]',
                                                       exceptions=(NoSuchElementException,),
                                                       timeout=0.1)
        phone_number = phone_number_element.text
        self._driver.find_element(By.CLASS_NAME, "close_ad").click()
        return phone_number

    def get_predicated_products(self, url: str, *predicates):
        products = []
        web_elements = self._get_web_elements(url)
        for web_element in web_elements:
            for predicate in predicates:
                product_details = Yad2._get_details(web_element)
                if predicate(product_details):
                    products.append(Product(product_details, self._get_phone_number(web_element)))
        return products

    @staticmethod
    def _get_details(web_element: WebElement):
        return Details(web_element.find_element(By.CLASS_NAME, "title").text,
                       web_element.find_element(By.CLASS_NAME, "area").text,
                       web_element.find_element(By.CLASS_NAME, "price").text)
