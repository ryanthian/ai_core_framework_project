from decimal import Decimal


TRANSACTIONS = [
    {"id": "txn-1", "category": "food", "amount": "10.00", "owner_id": "user-1"},
    {"id": "txn-2", "category": "ads", "amount": "25.00", "owner_id": "user-1"},
    {"id": "txn-3", "category": "food", "amount": "40.00", "owner_id": "user-2"},
]


def normalize_category(category):
    return category.strip().lower()


def filter_transactions_by_category(rows, category):
    if category == "":
        return list(rows)
    expected = normalize_category(category)
    return [row for row in rows if normalize_category(row.get("category", "")) == expected]


def filter_transactions_by_amount_range(rows, minimum=None, maximum=None):
    min_amount = Decimal(minimum) if minimum is not None else None
    max_amount = Decimal(maximum) if maximum is not None else None
    result = []
    for row in rows:
        amount = Decimal(row["amount"])
        if min_amount is not None and amount < min_amount:
            continue
        if max_amount is not None and amount > max_amount:
            continue
        result.append(row)
    return result

