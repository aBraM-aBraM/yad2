from typing import Iterable

import consts
from structs import Details


def contains_tokens(tokens: Iterable[str]):
    return lambda x: any([token.lower() in x.title.lower() for token in tokens])


def min_price(minimum_price: int):
    return lambda x: x.price > minimum_price


def max_price(maximum_price: int):
    return lambda x: x.price < maximum_price
