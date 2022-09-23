def price_range(minimum_price: int, maximum_price: int):
    return f"&price={minimum_price}-{maximum_price}"


def min_price(minimum_price: int):
    return price_range(minimum_price, -1)


def max_price(maximum_price: int):
    return price_range(0, maximum_price)
