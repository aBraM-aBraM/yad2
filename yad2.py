import time
from typing import List

import consts
import utils

from selenium.webdriver.common.by import By
import re

from undetected_chromedriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from structs import Details, Product


class Yad2:
    YAD2_ITEM_PATTERN = re.compile(r"^feed_item_\d+\b")  # item id regex

    def __init__(self, driver, url):
        self._driver = driver
        self._base_url = url

    def _get_items_elements(self) -> List[WebElement]:
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

    def _get_page_count(self) -> int:
        return int(self._driver.find_element(By.XPATH, '//button[@class="page-num"]').text)

    def get_predicated_products(self, *predicates) -> List[Product]:
        products = []

        self._driver.get(self._base_url)
        page_count = self._get_page_count()

        for page_number in range(1, page_count + 1):
            # get the current page
            self._driver.get("{url}&page={page_number}".format(url=self._base_url, page_number=page_number))

            items_elements = self._get_items_elements()
            for item_element in items_elements:
                for predicate in predicates:
                    product_details = Yad2._get_details(item_element)
                    if predicate(product_details):
                        products.append(Product(product_details, self._get_phone_number(item_element)))

        return products

    @staticmethod
    def _get_details(web_element: WebElement) -> Details:
        return Details(web_element.find_element(By.CLASS_NAME, "title").text,
                       web_element.find_element(By.CLASS_NAME, "area").text,
                       web_element.find_element(By.CLASS_NAME, "price").text)
