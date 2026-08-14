# Orders API

POST /orders

Authentication: Bearer token required.

Request fields: customer_id, sku, quantity.

Success response: 201 with order_id and status.

Error response: 400 for invalid quantity and 401 for missing authentication.

Timeout behavior not specified.

Idempotency not specified.
