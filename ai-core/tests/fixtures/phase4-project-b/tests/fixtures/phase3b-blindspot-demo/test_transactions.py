import unittest

from transactions import TRANSACTIONS, filter_transactions_by_date_range


class DateRangeFilterTest(unittest.TestCase):
    def test_inclusive_date_bounds(self):
        rows = filter_transactions_by_date_range(TRANSACTIONS, "2026-08-01", "2026-08-15")

        self.assertEqual([row["id"] for row in rows], ["txn-1", "txn-2"])

    def test_empty_matching_range(self):
        rows = filter_transactions_by_date_range(TRANSACTIONS, "2026-07-01", "2026-07-31")

        self.assertEqual(rows, [])

    def test_start_after_end_returns_empty(self):
        rows = filter_transactions_by_date_range(TRANSACTIONS, "2026-08-31", "2026-08-01")

        self.assertEqual(rows, [])

    def test_invalid_date_raises_value_error(self):
        with self.assertRaises(ValueError):
            filter_transactions_by_date_range(TRANSACTIONS, "08/01/2026", "2026-08-31")


if __name__ == "__main__":
    unittest.main()

