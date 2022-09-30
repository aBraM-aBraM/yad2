import pathlib
import traceback

import logging
import argparse

from src import consts
from src import predicates
from src import query_predicates
from src.telegram_bot import TelegramBot
from src.yad2_scanner import Yad2Scanner


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--chrome-driver", help="path to chromedriver", required=True, type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        logging.basicConfig(filename=consts.PROJECT_DIR / "yad2.log",
                            filemode="w",
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            level=logging.INFO,
                            datefmt="%Y-%m-%d %H:%M:%S")

        try:
            with open(consts.SECRETS_DIR / "bot_token.secret") as token_fd:
                token = token_fd.read().strip()
        except IOError:
            logging.critical("Couldn't read the bot's token")
            exit(1)

        scanner = Yad2Scanner(consts.ELECTRIC_GUITARS_URL,
                              chromedriver_path=args.chrome_driver,
                              predicates=[predicates.contains_tokens(consts.FENDER_TOKENS)],
                              query_predicates=[query_predicates.price_range(4000, 7000)])
        bot = TelegramBot(token, scanner)
        bot.serve()

    except Exception as e:
        logging.critical(e)
        logging.critical(traceback.format_exc())


if __name__ == '__main__':
    main()
