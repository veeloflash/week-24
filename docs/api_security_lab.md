# API Security Lab Evidence

These checks execute the real FastAPI routes, token lookup, SQLite user lookup, and authorization logic. Run them from the repository root with:

```bash
pytest -q tests/test_api_security_integration.py
```

| Test | Expected | Actual |
|---|---:|---:|
| User A login, token, then own `/api/progress/{A}` | 200 | 200 |
| User A token on another user's `/api/progress/{B}` | 403 | 403 |
| Invalid token on protected progress endpoint | 401 | 401 |

The regression test covers login, token issuance, database-backed authentication, own-resource access, cross-user denial, and invalid-token denial without mocking those boundaries.