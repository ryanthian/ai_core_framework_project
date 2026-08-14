import unittest

from transactions import export_transactions_csv


class ExportTransactionsCsvTest(unittest.TestCase):
    def test_exports_header_and_rows_in_stable_order(self):
        csv_text = export_transactions_csv(
            [
                {
                    "id": "txn-1",
                    "date": "2026-08-14",
                    "description": "Affiliate payout",
                    "amount": "120.50",
                }
            ]
        )

        self.assertEqual(
            csv_text,
            "id,date,description,amount\r\ntxn-1,2026-08-14,Affiliate payout,120.50\r\n",
        )

    def test_quotes_values_containing_commas(self):
        csv_text = export_transactions_csv(
            [
                {
                    "id": "txn-2",
                    "date": "2026-08-14",
                    "description": "Ads, August",
                    "amount": "-40.00",
                }
            ]
        )

        self.assertIn('"Ads, August"', csv_text)

    def test_empty_input_returns_header_only(self):
        self.assertEqual(export_transactions_csv([]), "id,date,description,amount\r\n")

    def test_missing_values_export_as_empty_cells(self):
        csv_text = export_transactions_csv([{"id": "txn-3", "amount": "9.00"}])

        self.assertEqual(csv_text, "id,date,description,amount\r\ntxn-3,,,9.00\r\n")


if __name__ == "__main__":
    unittest.main()

