import sqlite3

DB_NAME = "resume_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME,timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        score INTEGER,
        skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_resume(filename, score, skills):
    conn = sqlite3.connect(DB_NAME,timeout=10)
    cursor = conn.cursor()

    skills_text = ", ".join(skills)

    cursor.execute("""
    INSERT INTO resumes (filename, score, skills)
    VALUES (?, ?, ?)
    """, (filename, score, skills_text))

    conn.commit()
    conn.close()


def get_all_resumes():

    conn = sqlite3.connect(DB_NAME, timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT filename, score, skills, created_at
    FROM resumes
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows