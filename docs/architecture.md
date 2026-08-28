# Architecture — AI Learning Platform V2

## 1. Overview

AI Learning Platform V2 是一个完整的全栈学习系统，包含：

- 前端（HTML + JavaScript）
- 后端（FastAPI）
- 数据库（SQLite）
- 模型网关（Model Gateway）
- 权限系统（RBAC + Ownership + Teacher Assignment）
- 安全链（transport/schema parsing → rate limit → authentication → authorization → business validation → operation → error handling）
- 测试套件（pytest）

系统目标：  
为学生、老师、管理员提供一个安全、可扩展、可验证的学习平台。

---

## 2. System Architecture Diagram

```
Browser (Frontend)
↓
FastAPI (Backend)
↓
Authentication (token → user)
↓
Authorization (role + ownership + teacher assignment)
↓
Validation (input schema + custom rules)
↓
Rate Limit (per-token)
↓
Model Gateway / Database
↓
Error Handling (safe JSON)
↓
Response
```

---

## 3. Backend Structure

```
backend/
main.py
auth.py
permissions.py
database.py
model_gateway.py
routes/
users.py
progress.py
studyplan.py
assign.py
security/
validation.py
rate_limit.py
errors.py
```

---

## 4. Frontend Structure

```
frontend/
index.html
app.js
style.css
```

前端通过 fetch 调用后端 API，实现：

- 登录  
- 查看进度  
- 查看学习计划  
- 调用模型网关生成学习计划  

---

## 5. Database Schema

### users
| id | username | password_hash | role |
|----|----------|----------|------|
| PK | TEXT     | TEXT     | student/teacher/admin |

### progress
| id | user_id | percentage |
|----|---------|------------|

### studyplan
| id | user_id | content |
|----|---------|---------|

### teacher_students
| id | teacher_id | student_id |
|----|------------|------------|

---

## 6. Model Gateway

模型网关统一管理所有模型调用：

```python
def call_model(prompt, context):
    if "study plan" in prompt.lower():
        return "Weekly Study Plan: 1) Review notes 2) Practice problems 3) Take a quiz."
    return "Model response placeholder."
```
它是用于测试架构和权限的 mock；外部模型集成不在 Week24 范围内。它被保护在：
- Rate Limit
- Authentication
- Validation
- Error Handling
CORS / transport parsing
↓
Rate Limit Middleware
↓
Authentication
↓
Authorization
↓
Business validation
↓
Business Logic (DB / Model)
↓
Error Handling (safe JSON)
Validation
↓
Business Logic (DB / Model)
↓
Error Handling
↓
Response
```
## 8. Scope
This architecture is a Week24 educational prototype. It demonstrates security boundaries locally but does not claim production deployment readiness.