import unittest

from cart import cart_total, line_total


class LineTotalTest(unittest.TestCase):
    def test_one_item_pays_full_price(self):
        self.assertEqual(line_total(10.0, 1), 10.0)

    def test_three_items_get_the_bulk_discount(self):
        self.assertEqual(line_total(10.0, 3), 27.0)

    def test_five_items_get_the_bulk_discount(self):
        self.assertEqual(line_total(10.0, 5), 45.0)


class CartTotalTest(unittest.TestCase):
    def test_mixed_cart(self):
        self.assertEqual(cart_total([(10.0, 3), (2.5, 2)]), 32.0)


if __name__ == "__main__":
    unittest.main()