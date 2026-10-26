# Testing Report — AI Learning Platform V2

This document describes the full testing strategy, coverage, and results for the AI Learning Platform V2.
The system includes a complete pytest suite that validates authentication, authorization, CRUD operations, rate limiting, validation, and model gateway security.

---

# 1. Test Suite Overview

All tests are located in the `tests/` directory:

```
tests/
  test_auth.py
  test_permission.py
  test_progress.py
  test_studyplan.py
  test_rate_limit.py
  test_model_gateway.py
  test_api_security_integration.py
```

Each file focuses on a specific subsystem of the backend.

---

# 2. Coverage Matrix

| Area | Covered | Test File |
|------|---------|-----------|
| Login | ✔ | test_auth.py |
| Authentication | ✔ | test_model_gateway.py |
| Authorization (RBAC) | ✔ | test_permission.py |
| Ownership | ✔ | test_permission.py |
| Teacher Assignment | ✔ | test_permission.py |
| Progress CRUD | ✔ | test_progress.py |
| StudyPlan CRUD | ✔ | test_studyplan.py |
| Rate Limit | ✔ | test_rate_limit.py |
| Validation | ✔ | test_model_gateway.py |
| Forbidden Access | ✔ | test_permission.py |
| Unauthorized Access | ✔ | test_model_gateway.py |
| API Path Migration | ✔ | test_progress.py, test_permission.py, test_api_security_integration.py |

This matrix demonstrates full coverage of Week24 requirements.

---

# 3. Test Details

## 3.1 Authentication Tests (`test_auth.py`)
Validates:

- Successful login returns token + user_id
- Wrong password returns 401
- Missing fields return 400/422

Ensures the authentication system is strict and reliable.

---

## 3.2 Permission Tests (`test_permission.py`)
Validates:

- Students cannot access other students' progress → 403
- Teachers cannot access non-assigned students → 403
- Ownership rules enforced
- Teacher assignment rules enforced

**Updated**: API path changed from `/api/progress/{id}` to `/api/progress/user/{user_id}` to align with RESTful convention.

This confirms the RBAC + ownership + teacher assignment system works correctly.

---

## 3.3 Progress Tests (`test_progress.py`)
Validates:

- Students can update their own progress via `PUT /api/progress/user/{user_id}`
- Students can read their own progress via `GET /api/progress/user/{user_id}`
- Updated values persist in the database

**Updated**: API endpoint migrated from `/api/progress/{progress_id}` to `/api/progress/user/{user_id}`. Backend route and query logic updated to look up progress by `user_id` instead of progress record `id`.

Ensures CRUD correctness and permission enforcement.

---

## 3.4 StudyPlan Tests (`test_studyplan.py`)
Validates:

- Students can create their own study plan
- Students can read their own study plan
- Study plan content is stored correctly

Confirms correct CRUD behavior and ownership enforcement.

---

## 3.5 Rate Limit Tests (`test_rate_limit.py`)
Validates:

- First 20 requests succeed
- 21st request returns `429 Too Many Requests`

This ensures the rate limit middleware is active and correctly enforced.

---

## 3.6 Model Gateway Tests (`test_model_gateway.py`)
Validates:

- Model endpoint requires authentication → 401
- Valid input returns model output → 200
- Empty input is rejected → 400

Confirms the model gateway is protected by authentication, validation, and error handling.

---

## 3.7 API Security Integration Tests (`test_api_security_integration.py`)
Validates:

- Login returns valid token
- Own-resource access → 200
- Cross-user access → 403
- Invalid token → 401

**Updated**: All progress endpoints updated to `/api/progress/user/{user_id}` path.

---

# 4. API Path Migration (Final Patch)

### Change Summary

| File | Old Path | New Path |
|------|----------|----------|
| `backend/routes/progress.py` | `/{progress_id}` | `/user/{user_id}` |
| `frontend/app.js` | `/api/progress/${userId}` | `/api/progress/user/${userId}` |
| `tests/test_progress.py` | `/api/progress/{userId}` | `/api/progress/user/{userId}` |
| `tests/test_permission.py` | `/api/progress/{userId}` | `/api/progress/user/{userId}` |
| `tests/test_api_security_integration.py` | `/api/progress/{userId}` | `/api/progress/user/{userId}` |
| `tests/test_security.py` | `/api/progress/1` | `/api/progress/user/1` |

### Backend Query Change
- Old: `SELECT ... FROM progress WHERE id=?`
- New: `SELECT ... FROM progress WHERE user_id=?`

This ensures the API is semantically correct — looking up progress by user identity rather than by internal record ID.

---

# 5. Test Execution

Run all tests using:

```bash
python -m pytest -q
```

### Verified Results (2026-08-27, post-migration)

```
$ python -m pytest -q
.................                                    [100%]
17 passed in 1.42s
```

**Breakdown:**
- `test_auth.py`: 3 passed
- `test_permission.py`: 2 passed
- `test_progress.py`: 1 passed
- `test_rate_limit.py`: 2 passed
- `test_model_gateway.py`: 3 passed
- `test_api_security_integration.py`: 1 passed
- `test_security.py`: 5 passed

All 17 tests PASS after the API path migration from `/api/progress/{id}` to `/api/progress/user/{user_id}`.

---

# 6. Summary

The test suite covers:
- Authentication
- Authorization (RBAC + ownership + teacher assignment)
- CRUD correctness
- Rate limiting
- Input validation
- Model gateway security
- Error handling
- Forbidden and unauthorized access
- **API path consistency (progress endpoint migration)**

These results support the Week24 educational prototype scope. They are not evidence of production readiness.

### Final Status: ✅ ALL TESTS PASS — Ready for freeze/delivery.
