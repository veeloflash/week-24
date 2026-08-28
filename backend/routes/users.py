from fastapi import APIRouter, HTTPException
from backend.models import UserLogin
from backend.database import get_db # pyright: ignore[reportAttributeAccessIssue]
from backend.utils.hashing import hash_password, verify_password
from backend.utils.tokens import generate_token

router = APIRouter()

@router.post("/register")
def register(user: UserLogin):
    conn = get_db()
    cur = conn.cursor()

    hashed = hash_password(user.password)

    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (user.username, hashed, "student")
        )
        conn.commit()
    except Exception:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    conn.close()
    return {"message": "User registered"}

@router.post("/login")
def login(user: UserLogin):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password_hash, role FROM users WHERE username=?",
        (user.username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_hash = row[1]
    if not verify_password(user.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = generate_token(row[0])
    return {"token": token, "user_id": row[0], "role": row[2]}
