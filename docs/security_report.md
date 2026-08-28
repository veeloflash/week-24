# Security Report — AI Learning Platform V2

This Week24 educational security prototype demonstrates authentication, action-aware authorization, ownership checks, validation, rate limiting, and safe errors. It is not production-ready.

---

# 1. Security Chain Overview

Requests pass through these relevant layers:
```
Transport/schema parsing
↓
Rate Limit Middleware
↓
Authentication (token → user)
↓
Authorization (role + action + ownership/assignment)
↓
Business validation
↓
Business Logic (DB / mock model gateway)
↓
Error Handling (safe JSON)
```

This chain ensures that *no request can bypass security*, even if the route is misconfigured.

---

# 2. Authentication

Implemented in `backend/auth.py`.

### Mechanism
- Token-based authentication.
- User logs in via `/api/users/login`.
- Backend returns:
  - `token`
  - `user_id`
  - `role`

### Security Rules
- Missing token → `401 Unauthorized`
- Invalid token → `401 Unauthorized`
- Token maps to a user in the database.

### Why it matters
Authentication ensures that every request is tied to a real user identity.

---

# 3. Authorization (RBAC + Ownership + Teacher Assignment)

Implemented in `backend/permissions.py`.

### Role Matrix

| Role     | Allowed Actions |
|----------|-----------------|
| student  | Read/update own progress; read/create own study plans |
| teacher  | Read assigned students' resources |
| admin    | All defined actions |

### Ownership Enforcement
Students can only access their own:

- progress  
- studyplan  

If a student tries to access another student's resource → `403 Forbidden`.

### Teacher Assignment
Teachers must be explicitly assigned to students:

```
POST /api/assign/{teacher_id}/{student_id}
```

If a teacher tries to access a non-assigned student → `403 Forbidden`.

### Admin
Admins bypass ordinary ownership restrictions, but still require authentication and do not bypass validation, rate limits, error handling, or other controls.

### Why it matters
Authorization prevents horizontal privilege escalation and ensures strict resource isolation.

---

# 4. Input Validation

Implemented in `backend/security/validation.py`.

### Validation Rules
- Empty input → `400 Bad Request`
- Input longer than 1000 chars → `400 Bad Request`
- Progress percentage must be 0–100 → `400 Bad Request`

### Validation Applied To
- Model Gateway (`/api/model/generate`)
- StudyPlan creation
- Progress update

### Why it matters
Validation prevents malformed input, prompt injection attempts, and accidental misuse.

---

# 5. Rate Limiting

Implemented in `backend/security/rate_limit.py`.

### Rules
- Each token can make **20 requests per minute**.
- The **21st request** returns:
```
429 Too Many Requests
```

### Why it matters
Rate limiting prevents:

- Abuse  
- Infinite loops  
- Scripted attacks  
- Model spamming  

---

# 6. Error Handling

Implemented in `backend/security/errors.py`.

### Handled Exceptions
- `HTTPException` → returns status + detail
- `ValidationError` → returns `400 Invalid input format`
- Generic `Exception` → returns `500 Internal server error`

### Security Benefits
- No stack traces leak to the client  
- No internal error messages  
- All errors return safe JSON  
- Prevents information disclosure  

---

# 7. Model Gateway Security

Model Gateway (`/api/model/generate`) is a deterministic mock protected by:

### ✔ Authentication  
Token required.

### ✔ Authorization  
Can be extended to role-based model access.

### ✔ Validation  
Prompt must be non-empty and safe.

### ✔ Rate Limit  
Model calls count toward the 20/min limit.

### ✔ Error Handling  
All model errors return safe JSON.

External model integration, API-key lifecycle, timeout, cost controls, and output validation are outside this prototype's scope.

---

# 8. Teacher–Student Assignment Security

Teacher assignment is stored in:

```
teacher_students (teacher_id, student_id)
```

Security rules:

- Only admin can assign students.
- Teacher can only access assigned students.
- Students cannot assign themselves.

This prevents unauthorized access to student data.

---

# 9. Summary

This is a Week24 educational security prototype demonstrating authentication, authorization, ownership checks, validation, rate limiting, and safe errors. It is not production-ready.