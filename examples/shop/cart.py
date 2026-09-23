BULK_THRESHOLD = 3
BULK_DISCOUNT = 0.10


def line_total(price: float, quantity: int) -> float:
    """Price for one line of the cart. Buying three or more of an item takes 10% off that line."""
    total = price * quantity
    if quantity > BULK_THRESHOLD:
        total = total * (1 - BULK_DISCOUNT)
    return round(total, 2)


def cart_total(lines: list) -> float:
    """Sum of every line. Each line is a (price, quantity) pair."""
    return round(sum(line_total(price, quantity) for price, quantity in lines), 2)