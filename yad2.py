import logging
from typing import List, Callable

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from undetected_chromedriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import utils
from structs import Details


class Yad2:
    YAD2_ITEM_PATTERN = re.compile(r"^feed_item_\d+\b")  # item id regex

    def __init__(self, driver: undetected_chromedriver.Chrome, url: str):
        self._driver = driver
        self._base_url = url

    def _get_items_elements(self) -> List[BeautifulSoup]:
        page_elements = [web_element for web_element in
                         self._driver.find_element(By.CLASS_NAME, "feed_list").find_elements(By.CSS_SELECTOR, "*")
                         if Yad2.YAD2_ITEM_PATTERN.match(web_element.get_attribute("id"))]
        return [BeautifulSoup(web_element.get_attribute("innerHTML"), "html.parser") for web_element in page_elements]

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

    def get_predicated_products(self, *predicates: Callable[[Details], bool], max_pages=0) -> List[Details]:
        products = []

        self._driver.get(self._base_url)
        page_count = self._get_page_count()
        logging.info(f"{page_count} pages founded, starting to gather items")

        max_pages = page_count + 1 if not max_pages else min(max_pages + 1, page_count + 1)

        for page_number in range(1, max_pages):
            # get the current page
            self._driver.get("{url}&page={page_number}".format(url=self._base_url, page_number=page_number))
            items_elements = self._get_items_elements()

            logging.info(f"loaded page {page_number}")
            for item_element in items_elements:
                product_details = Yad2._get_details(item_element)
                if any([predicate(product_details) for predicate in predicates]):
                    logging.info(f"adding matching item {product_details}")
                    products.append(product_details)

        return products

    @staticmethod
    def _get_details(web_element: BeautifulSoup) -> Details:
        return Details(web_element.find(class_="title").text,
                       web_element.find(class_="area").text,
                       web_element.find(class_="price").text.partition('₪')[0].replace(",", "").strip())
