from typing import Iterable

import consts
from structs import Details


def contains_tokens(item_details: Details, tokens: Iterable[str]):
    return any([token.lower() in item_details.title.lower() for token in tokens])


def is_fender(item_details: Details):
    return contains_tokens(item_details, consts.FENDER_TOKENS)
