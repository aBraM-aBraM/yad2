import contextlib
import logging
from typing import List, Callable, Set

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from undetected_chromedriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import utils
from src import consts
from structs import Details


class Yad2Scanner:
    YAD2_ITEM_PATTERN = re.compile(r"^feed_item_\d+\b")  # item id regex

    def __init__(self, url: str,
                 predicates: List[Callable[[Details], bool]] = tuple(),
                 query_predicates: List[str] = tuple()):
        self._driver = None
        self._base_url = url
        self._current_url = None
        self._predicates = predicates
        self._query_predicates = query_predicates

        self._last_scan: List[Details] = []

    @contextlib.contextmanager
    def _get_driver(self):
        options = undetected_chromedriver.ChromeOptions()

        # setting profile
        options.user_data_dir = consts.PROFILE_PATH

        # just some options passing in to skip annoying popups
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

        driver = undetected_chromedriver.Chrome(options=options, driver_executable_path=r"D:\chromedriver.exe")
        driver.implicitly_wait(10)

        self._driver = driver
        yield
        self._driver.close()

    @property
    def last_scan(self):
        return self._last_scan

    def _get_items_elements(self) -> List[BeautifulSoup]:
        return [web_element for web_element in
                BeautifulSoup(self._driver.find_element(By.CLASS_NAME, "feed_list").get_attribute("innerHTML"),
                              "html.parser").find_all(class_="feeditem") if
                web_element.contents[0].get("item-id") is not None]

    def get_phone_number(self, url: str) -> str:
        with self._get_driver():
            logging.info(f"getting phone number from {url}")
            self._driver.get(url)

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
        return phone_number

    def _get_page_count(self) -> int:
        return int(self._driver.find_element(By.XPATH, '//button[@class="page-num"]').text)

    def _load_page(self, url: str, query_predicates_str: str, page_number: int = None):

        self._current_url = f"{url}{query_predicates_str}"
        if page_number:
            self._current_url += f"&page={page_number}"
        logging.info(f"loading {self._current_url}")
        self._driver.get(self._current_url)

    def scan(self, max_pages: int = 0, predicates: List[Callable[[Details], bool]] = tuple(),
             query_predicates: List[str] = tuple()) -> Set[Details]:
        with self._get_driver():
            products = set()
            query_predicates_str = ''.join(list(query_predicates) + self._query_predicates)

            self._load_page(self._base_url, query_predicates_str)

            page_count = self._get_page_count()
            logging.info(f"{page_count} pages founded, starting to gather items")

            max_pages = page_count + 1 if not max_pages else min(max_pages + 1, page_count + 1)

            for page_number in range(1, max_pages):
                # get the current page
                self._load_page(self._base_url, query_predicates_str, page_number)
                items_elements = self._get_items_elements()

                logging.info(f"loaded page {page_number}")
                for item_element in items_elements:
                    try:
                        product_details = self._get_details(item_element)
                    except ValueError:
                        # ignore products with no given price
                        continue
                    if predicates is not None:
                        if all([predicate(product_details) for predicate in (list(predicates) + self._predicates)]):
                            logging.info(f"adding matching item {product_details.title}")
                            products.add(product_details)
                    else:
                        products.add(product_details)
            self._last_scan = products
        return products

    def _get_item_link(self, web_element: BeautifulSoup):
        return self._current_url + f"&open-item-id={web_element.contents[0]['item-id']}&categoryId=3&view=light-box"

    def _get_details(self, web_element: BeautifulSoup) -> Details:
        return Details(title=web_element.find(class_="title").text,
                       price=int(web_element.find(class_="price").text.partition('₪')[0].replace(",", "").strip()),
                       link=self._get_item_link(web_element),
                       area=web_element.find(class_="area").text,
                       picture=web_element.find(class_="feedImage")["src"])
