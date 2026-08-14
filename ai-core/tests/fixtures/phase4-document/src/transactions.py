def export_accounts_json(accounts):
    return [{"id": row["id"], "owner": row["owner"], "balance": row["balance"]} for row in accounts]
