# Test Evidence

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 -m unittest discover -s tests`

Expected: PASS

Actual: FAIL

```text
.E
======================================================================
ERROR: test_merchant_filter (test_transactions.TransactionTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ryanthian/Documents/Codex_mac/ai-core/tests/fixtures/phase4-test-failure/tests/test_transactions.py", line 7, in test_merchant_filter
    self.assertEqual(filter_transactions(rows, "Alpha"), [{"merchant":"Alpha","amount":4}])
  File "/Users/ryanthian/Documents/Codex_mac/ai-core/tests/fixtures/phase4-test-failure/src/transactions.py", line 2, in filter_transactions
    return [row for row in transactions if row.get('amount', 0) >= min_amount]
  File "/Users/ryanthian/Documents/Codex_mac/ai-core/tests/fixtures/phase4-test-failure/src/transactions.py", line 2, in <listcomp>
    return [row for row in transactions if row.get('amount', 0) >= min_amount]
NameError: name 'min_amount' is not defined

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (errors=1)

```
