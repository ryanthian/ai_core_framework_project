import unittest

from transactions import TRANSACTION_FIELDS, export_transactions_csv, export_transactions_json, normalize_transaction_rows


class ExportTransactionsCsvTest(unittest.TestCase):
    def test_transaction_fields_are_fixed(self):
        self.assertEqual(TRANSACTION_FIELDS, ["id", "date", "description", "amount"])

    def test_csv_export_quotes_commas(self):
        csv_text = export_transactions_csv(
            [{"id": "txn-1", "date": "2026-08-15", "description": "Ads, August", "amount": "42.00"}]
        )
        self.assertIn('"Ads, August"', csv_text)

    def test_empty_input_returns_header_only(self):
        self.assertEqual(export_transactions_csv([]), "id,date,description,amount\r\n")

    def test_normalize_transaction_rows_uses_fixed_fields(self):
        rows = normalize_transaction_rows(
            [{"id": "txn-2", "date": "2026-08-15", "description": "Bonus", "amount": "7.00", "extra": "ignored"}]
        )

        self.assertEqual(rows, [{"id": "txn-2", "date": "2026-08-15", "description": "Bonus", "amount": "7.00"}])

    def test_json_export_uses_same_fixed_fields(self):
        json_text = export_transactions_json(
            [{"id": "txn-3", "description": "Missing date", "amount": "5.00", "extra": "ignored"}]
        )

        self.assertEqual(json_text, '[{"id":"txn-3","date":"","description":"Missing date","amount":"5.00"}]')


if __name__ == "__main__":
    unittest.main()
