import dataclasses
import time

from selenium.webdriver.common.by import By
import re

from undetected_chromedriver.webelement import WebElement

import consts


@dataclasses.dataclass
class Details:
    title: str
    area: str
    price: str


@dataclasses.dataclass
class Item:
    details: Details
    phone: str


class Yad2:
    YAD2_ITEM_PATTERN = re.compile(r"^feed_item_\d+\b")  # item id regex

    def __init__(self, driver):
        self._driver = driver

    def _get_items(self, url):
        self._driver.get(url)

        return [item for item in
                self._driver.find_element(By.CLASS_NAME, "feed_list").find_elements(By.CSS_SELECTOR, "*")
                if Yad2.YAD2_ITEM_PATTERN.match(item.get_attribute("id"))]

    def _get_phone_number(self, item):
        image_element: WebElement = item.find_element(By.XPATH, '//div[starts-with(@id, "image_")]')
        image_element.click()
        time.sleep(1)
        self._driver.find_element(By.CLASS_NAME, 'lightbox_contact_seller_button').click()
        time.sleep(1)
        phone_number: WebElement = self._driver.find_element(By.XPATH, '//a[starts-with(@class, "phone_number")]')
        print(phone_number.text)

    def get_predicated_products(self, url: str, predicate):
        items = self._get_items(url)
        for item in items:
            print(self._get_details(item))
        self._get_phone_number(items[0])

    def _get_details(self, item):
        return Details(item.find_element(By.CLASS_NAME, "title").text,
                       item.find_element(By.CLASS_NAME, "area").text,
                       item.find_element(By.CLASS_NAME, "price").text)
