# AI Learning Platform V2

Week24 educational prototype demonstrating a FastAPI backend, browser frontend, token authentication, action-aware authorization, ownership checks, validation, rate limiting, and a mocked model gateway. It is not production-ready.

---

# 1. Features

## ✔ Authentication（认证）
- Token 登录系统  
- 用户登录后获得 token + user_id + role  
- 所有 API 需要 token 才能访问  

## ✔ Authorization（权限系统）
- RBAC（学生 / 老师 / 管理员）  
- Ownership（学生只能访问自己的数据）  
- Teacher Assignment（老师只能访问被分配的学生）  
- Admin 拥有全部权限  

## ✔ StudyPlan（学习计划）
- 创建学习计划  
- 查看学习计划  
- 输入验证（防止空内容、过长内容）  

## ✔ Progress（学习进度）
- 更新进度  
- 查看进度  
- 输入验证（百分比必须 0–100）  

## ✔ Model Gateway（模型网关）
- Mock model gateway protected by authentication, validation, and rate limiting
- External model integration is out of scope for this educational prototype
- 输入验证  
- 限流保护  
- 错误处理保护  

## ✔ Security Chain（安全链）
请求处理顺序区分为：

```
Transport/schema parsing → Rate Limit → Authentication → Authorization → Business validation → Operation → Error handling
```

## ✔ Frontend（前端）
- 简洁 UI  
- 登录  
- 查看进度  
- 查看学习计划  
- 调用模型网关生成学习计划  

## ✔ Testing（测试）
完整 pytest 测试覆盖：

- Auth  
- Permission  
- Ownership  
- Teacher Assignment  
- Progress CRUD  
- StudyPlan CRUD  
- Rate Limit  
- Validation  
- Model Gateway  

---

# 2. Project Structure

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

frontend/
index.html
app.js
style.css

tests/
test_auth.py
test_permission.py
test_progress.py
test_studyplan.py
test_rate_limit.py
test_model_gateway.py

docs/
Architecture.md
Security_Report.md
Testing_Report.md
README.md
```

---

# 3. Running the Backend

确保你在项目根目录：

```bash
uvicorn backend.main:app --reload
```
API 文档：

```
http://127.0.0.1:8000/docs
```

# 4. Running the Frontend
直接打开：

```
frontend/index.html
```

即就可一使用：

- 登录
- 查看进度
- 查看学习计划
- 调用模型网关

# 5. Running Tests

```bash
pytest
```

测试结果以实际 `pytest -q` 输出为准。

# 6. API Overview
Authentication
```
POST /api/users/login
```
StudyPlan
```
POST /api/studyplan/{user_id}
GET  /api/studyplan/{user_id}
```
Progress
```
PUT /api/progress/{user_id}
GET /api/progress/{user_id}
```
Teacher Assignment
```
POST /api/assign/{teacher_id}/{student_id}
```
Model Gateway
```
POST /api/model/generate
```
# 7. Security Summary
系统实现：

- Token 认证
- RBAC 权限系统
- Ownership
- Teacher Assignment
- 输入验证
- 限流
- 全局错误处理
- 模型网关安全保护
- 所有安全模块均有测试覆盖。

# 8. Security and data notes
- Passwords are never stored as plaintext; users use salted PBKDF2 password hashes in `password_hash`.
- The SQLite database and in-memory tokens are suitable for local learning only.
- See `docs/api_security_lab.md` for executable authorized/unauthorized API evidence.