import csv
import io
import json


TRANSACTION_FIELDS = ["id", "date", "description", "amount"]


def export_transactions_csv(rows):
    """Return transaction rows as CSV text with a stable column order."""
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=TRANSACTION_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in normalize_transaction_rows(rows):
        writer.writerow(row)
    return output.getvalue()


def normalize_transaction_rows(rows):
    """Return rows reduced to the approved transaction export fields."""
    return [{field: row.get(field, "") for field in TRANSACTION_FIELDS} for row in rows]


def export_transactions_json(rows):
    """Return transaction rows as deterministic JSON text."""
    return json.dumps(normalize_transaction_rows(rows), ensure_ascii=True, separators=(",", ":"))
