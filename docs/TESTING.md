# Testing & Evidence Plan

## Functional cases

| Test | Expected |
|---|---|
| Benign informational prompt | ALLOW |
| SQL injection payload | BLOCK |
| XSS payload | BLOCK |
| Directory traversal payload | BLOCK |
| Command injection payload | BLOCK |
| Prompt injection payload | BLOCK |

## Automated tests

`backend/tests/test_gateway.py` covers benign traffic and representative malicious payloads.

## Evidence to capture for the final presentation

1. Dashboard loaded with system status operational.
2. Benign request returning ALLOW.
3. SQL injection returning BLOCK.
4. XSS returning BLOCK.
5. Prompt injection returning BLOCK.
6. Security Event Stream showing stored events.
7. Terminal output of `pytest -q`.
8. Terminal output of `python evaluate.py`.
