def filter_transactions(transactions, merchant):
    return [row for row in transactions if row.get('merchant') == merchant]


def filter_amount_range(transactions, min_amount, max_amount):
    return [row for row in transactions if min_amount <= row.get('amount', 0) <= max_amount]
