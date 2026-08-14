# Test Evidence

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 -m unittest discover -s tests`

Expected: PASS

Actual: FAIL

```text
F.
======================================================================
FAIL: test_amount_range (test_transactions.TransactionTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/ryanthian/Documents/Codex_mac/ai-core/tests/fixtures/phase4-test-failure/tests/test_transactions.py", line 11, in test_amount_range
    self.assertEqual(filter_amount_range(rows, 5, 15), [{"merchant":"B","amount":12}])
AssertionError: Lists differ: [{'merchant': 'B', 'amount': 12}, {'merchant': 'C', 'amount': 20}] != [{'merchant': 'B', 'amount': 12}]

First list contains 1 additional elements.
First extra element 1:
{'merchant': 'C', 'amount': 20}

- [{'amount': 12, 'merchant': 'B'}, {'amount': 20, 'merchant': 'C'}]
+ [{'amount': 12, 'merchant': 'B'}]

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)

```
