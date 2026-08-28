import sqlite3
from backend.utils.hashing import hash_password

DB_PATH = "database/week24.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cur.fetchone():
        columns = {row[1] for row in cur.execute("PRAGMA table_info(users)")}
        if "password" in columns and "password_hash" not in columns:
            cur.execute("ALTER TABLE users RENAME COLUMN password TO password_hash")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS studyplan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        percentage INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacher_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY(teacher_id) REFERENCES users(id),
        FOREIGN KEY(student_id) REFERENCES users(id)
    )
    """)

    demo_users = [
        ("ming", hash_password("123"), "student"),
        ("tao", hash_password("123"), "student"),
        ("teacher", hash_password("123"), "teacher"),
        ("admin", hash_password("123"), "admin"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        demo_users,
    )
    cur.execute("SELECT id FROM users WHERE username IN (?, ?)", ("ming", "tao"))
    cur.executemany(
        "INSERT OR IGNORE INTO progress (user_id, percentage) VALUES (?, 0)",
        ((row[0],) for row in cur.fetchall()),
    )

    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_PATH)
