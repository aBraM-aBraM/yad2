from typing import Iterable


def contains_tokens(tokens: Iterable[str]):
    return lambda x: any([token.lower() in x.title.lower() for token in tokens])
