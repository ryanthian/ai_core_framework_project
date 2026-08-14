import unittest

from transactions import (
    TRANSACTIONS,
    filter_transactions_by_amount_range,
    filter_transactions_by_category,
    normalize_category,
)


class CategoryFilterTest(unittest.TestCase):
    def test_exact_category_match_returns_matching_rows(self):
        rows = filter_transactions_by_category(TRANSACTIONS, "food")
        self.assertEqual([row["id"] for row in rows], ["txn-1", "txn-3"])

    def test_unknown_category_returns_empty(self):
        self.assertEqual(filter_transactions_by_category(TRANSACTIONS, "travel"), [])

    def test_empty_category_returns_all_rows(self):
        self.assertEqual(filter_transactions_by_category(TRANSACTIONS, ""), TRANSACTIONS)

    def test_category_filter_does_not_mutate_rows(self):
        original = [dict(row) for row in TRANSACTIONS]
        filter_transactions_by_category(TRANSACTIONS, "food")
        self.assertEqual(TRANSACTIONS, original)


class AmountRangeFilterTest(unittest.TestCase):
    def test_inclusive_amount_bounds(self):
        rows = filter_transactions_by_amount_range(TRANSACTIONS, "10.00", "25.00")
        self.assertEqual([row["id"] for row in rows], ["txn-1", "txn-2"])

    def test_open_ended_minimum(self):
        rows = filter_transactions_by_amount_range(TRANSACTIONS, "25.00", None)
        self.assertEqual([row["id"] for row in rows], ["txn-2", "txn-3"])

    def test_open_ended_maximum(self):
        rows = filter_transactions_by_amount_range(TRANSACTIONS, None, "25.00")
        self.assertEqual([row["id"] for row in rows], ["txn-1", "txn-2"])


class NormalizedCategoryTest(unittest.TestCase):
    def test_normalize_category_strips_and_lowercases(self):
        self.assertEqual(normalize_category(" Food "), "food")

    def test_filter_uses_normalized_category(self):
        rows = filter_transactions_by_category(TRANSACTIONS, " Food ")
        self.assertEqual([row["id"] for row in rows], ["txn-1", "txn-3"])


if __name__ == "__main__":
    unittest.main()

