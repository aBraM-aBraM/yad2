import logging
from typing import Iterable
import pymongo
import hashlib

from src.structs import Details

ID_KEY = "_id"


class Database:

    def __init__(self, connection_db_path):
        try:
            with open(connection_db_path) as connection_str_fd:
                self._mongo_client = pymongo.MongoClient(connection_str_fd.read())
        except FileNotFoundError:
            logging.critical(f"Couldn't find connection string file {connection_db_path}")
            raise
        self._db = self._mongo_client.yad2
        self._items: pymongo.collection = self._db.items
        self._existing_items_ids = self._get_existing_ids()

    def _get_existing_ids(self):
        return set([item[ID_KEY] for item in self._items.find()])

    def add_items(self, items: Iterable[Details]):
        hashed_items = list()
        for item in items:
            if item.item_id not in self._existing_items_ids:
                hashed_items.append(item.__dict__)
                self._existing_items_ids.add(item.item_id)
                logging.info(f"added {item.title}")
            else:
                logging.info(f"{item.title} already exists, continuing")
        logging.info(f"adding a total of {len(hashed_items)} items")
        self._items.insert_many(hashed_items)
