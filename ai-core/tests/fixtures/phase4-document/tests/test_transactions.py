import unittest
from src.transactions import export_accounts_json

class ExportTests(unittest.TestCase):
    def test_json_export(self):
        self.assertEqual(export_accounts_json([{"id":"A1","owner":"R","balance":10}]), [{"id":"A1","owner":"R","balance":10}])

if __name__ == "__main__":
    unittest.main()
