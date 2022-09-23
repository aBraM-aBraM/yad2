from typing import Iterable

import consts
from structs import Details


def contains_tokens(tokens: Iterable[str]):
    return lambda x: any([token.lower() in x.title.lower() for token in tokens])
