import unittest
from src.transactions import filter_transactions, filter_amount_range

class TransactionTests(unittest.TestCase):
    def test_merchant_filter(self):
        rows = [{"merchant":"Alpha","amount":4}, {"merchant":"Beta","amount":12}]
        self.assertEqual(filter_transactions(rows, "Alpha"), [{"merchant":"Alpha","amount":4}])

    def test_amount_range(self):
        rows = [{"merchant":"A","amount":4}, {"merchant":"B","amount":12}, {"merchant":"C","amount":20}]
        self.assertEqual(filter_amount_range(rows, 5, 15), [{"merchant":"B","amount":12}])

if __name__ == "__main__":
    unittest.main()
