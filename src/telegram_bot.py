import json
import time
import traceback
from threading import Thread
from typing import Set

import telegram
from telegram import Update, ParseMode
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext

import logging
import urllib.parse

from src import consts
from src.structs import Details
from src.yad2_scanner import Yad2Scanner

YES = ["yes", "y"]
MEMBERS_CHAT_IDS_PATH = "../secrets/members_chat_ids.secret"

UNKNOWN_ERROR = 1
IL_TELEPHONE_CODE = "+972"


class TelegramBot:
    def __init__(self, token: str, scanner: Yad2Scanner):
        self._token = token
        self._updater = Updater(token=self._token, use_context=True)
        self._dispatcher = self._updater.dispatcher
        self._scanner = scanner
        self._clients = TelegramBot._load_clients()

        self._scan = True

    @staticmethod
    def _load_clients() -> Set[str]:
        try:
            with open(MEMBERS_CHAT_IDS_PATH) as members_chat_ids_fd:
                return set(json.load(members_chat_ids_fd))
        except FileNotFoundError:
            return set()

    def _add_client(self, client_chat_id: str):
        logging.info(f"new client {client_chat_id}")
        self._clients.add(client_chat_id)
        with open(MEMBERS_CHAT_IDS_PATH, "w+") as members_chat_ids_fd:
            json.dump(list(self._clients), members_chat_ids_fd)

    def _member_update(self, update: Update, context: CallbackContext):
        client_chat_id = str(update.effective_chat.id)

        if client_chat_id not in self._clients:
            context.bot.send_message(chat_id=client_chat_id, text="Hello there :)")
            self._add_client(client_chat_id)

            for item in self._scanner.last_scan:
                self._updater.bot.send_photo(chat_id=client_chat_id, photo=item.picture, caption=item.__repr__())
        else:
            TelegramBot.unknown(update, context)

    def handle_item_reply(self, update: Update, context: CallbackContext):

        if any([agreement in update.message.text.lower() for agreement in YES]):
            logging.info(f"handling item with caption {update.message.reply_to_message.caption.encode()}")
            try:
                item = Details(
                    *(update.message.reply_to_message.caption.splitlines() + [update.message.reply_to_message.photo]))

                phone_number = f"{IL_TELEPHONE_CODE}{self._scanner.get_phone_number(item.link).replace('-', '')[1:]}"
                msg_body = consts.ITEM_MESSAGE.format(item.title, item.price)
                text_link = f"<a href=\"https://wa.me/{phone_number}?text={urllib.parse.quote(msg_body)}\">Whatsapp</a>"

                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text_link,
                                         parse_mode=ParseMode.HTML,
                                         reply_to_message_id=update.message.message_id)
            except TypeError:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Cannot send, item is corrupted")
                logging.error(f"failed to fetch item {update.message.reply_to_message.caption}")
                logging.error(traceback.format_exc())
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Unknown message reply, reply to a photo of the item you're interested in "
                                          f"with {' or '.join(map(lambda x: f'<i>{x}</i>', YES))} "
                                          f"in order to send an sms to the seller",
                                     parse_mode=ParseMode.HTML)

    @staticmethod
    def unknown(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Unknown message, reply to a photo of the item you're interested in "
                                      f"with {' or '.join(map(lambda x: f'<i>{x}</i>', YES))} "
                                      f"in order to send an sms to the seller",
                                 parse_mode=ParseMode.HTML)

    def broadcast_item(self, item: Details):
        logging.info(f"broadcasting item with caption {item.title}")
        for client in self._clients:
            try:
                self._updater.bot.send_photo(chat_id=client, photo=item.picture, caption=item.__repr__())
            except telegram.error.BadRequest:
                logging.info(f"skipping item with no photo at {item.link}")

    def scan_loop(self):
        last_scanned_items = {}
        while self._scan:
            scanned_items = self._scanner.scan()
            new_items = scanned_items - scanned_items.intersection(last_scanned_items)
            logging.info(f"scanned new {len(scanned_items)} items")
            for item in new_items:
                self.broadcast_item(item)
            last_scanned_items = scanned_items.copy()
            time.sleep(3600)

    def serve(self):
        watch_thread = Thread(target=self.scan_loop)

        item_handler = MessageHandler(Filters.text & Filters.reply, self.handle_item_reply)
        self._dispatcher.add_handler(item_handler)

        member_update_handler = MessageHandler(Filters.all, self._member_update)
        self._dispatcher.add_handler(member_update_handler)

        watch_thread.start()
        self._updater.start_polling()
        logging.info("started serving")
        watch_thread.join()
