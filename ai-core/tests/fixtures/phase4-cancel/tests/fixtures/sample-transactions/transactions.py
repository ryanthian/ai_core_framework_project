import csv
import io


TRANSACTION_FIELDS = ["id", "date", "description", "amount"]


def export_transactions_csv(rows):
    """Return transaction rows as CSV text with a stable column order."""
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=TRANSACTION_FIELDS, extrasaction="ignore")
    writer.writeheader()

    for row in rows:
        writer.writerow({field: row.get(field, "") for field in TRANSACTION_FIELDS})

    return output.getvalue()

