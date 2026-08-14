from datetime import date


TRANSACTIONS = [
    {"id": "txn-1", "account_id": "acct-1", "owner_id": "user-1", "date": "2026-08-01", "amount": "10.00"},
    {"id": "txn-2", "account_id": "acct-1", "owner_id": "user-1", "date": "2026-08-15", "amount": "20.00"},
    {"id": "txn-3", "account_id": "acct-2", "owner_id": "user-2", "date": "2026-08-31", "amount": "30.00"},
]


def _parse_iso_date(value):
    return date.fromisoformat(value)


def filter_transactions_by_date_range(rows, start_date, end_date):
    """Return rows with dates between inclusive ISO date bounds."""
    start = _parse_iso_date(start_date)
    end = _parse_iso_date(end_date)
    if start > end:
        return []
    return [row for row in rows if start <= _parse_iso_date(row["date"]) <= end]

