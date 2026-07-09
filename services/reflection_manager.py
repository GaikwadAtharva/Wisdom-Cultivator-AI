import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            date TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            reflection_id INTEGER REFERENCES reflections(id) ON DELETE CASCADE,
            user_message TEXT NOT NULL,
            ai_message TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def create_reflection(user_id):
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    title = "New Reflection"
    date = datetime.now().strftime("%d %b %Y • %I:%M %p")

    cur.execute(
        "INSERT INTO reflections (user_id, title, date) VALUES (%s, %s, %s) RETURNING id",
        (user_id, title, date)
    )

    reflection_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return reflection_id


def get_all_reflections(user_id):
    init_db()

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM reflections WHERE user_id = %s ORDER BY id ASC",
        (user_id,)
    )

    reflections = cur.fetchall()

    for reflection in reflections:
        reflection["messages"] = get_messages(reflection["id"])

    cur.close()
    conn.close()

    return reflections


def get_reflection(user_id, reflection_id):
    init_db()

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT * FROM reflections WHERE id = %s AND user_id = %s",
        (reflection_id, user_id)
    )

    reflection = cur.fetchone()

    cur.close()
    conn.close()

    if reflection:
        reflection["messages"] = get_messages(reflection_id)

    return reflection


def get_messages(reflection_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        "SELECT user_message, ai_message FROM messages WHERE reflection_id = %s ORDER BY id ASC",
        (reflection_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    messages = []

    for row in rows:
        messages.append({
            "user": row["user_message"],
            "ai": row["ai_message"]
        })

    return messages


def add_message(user_id, reflection_id, user, ai):
    init_db()

    reflection = get_reflection(user_id, reflection_id)

    if reflection is None:
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages (reflection_id, user_message, ai_message) VALUES (%s, %s, %s)",
        (reflection_id, user, ai)
    )

    conn.commit()
    cur.close()
    conn.close()


def update_reflection_title(user_id, reflection_id, title):
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE reflections SET title = %s WHERE id = %s AND user_id = %s",
        (title, reflection_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def delete_reflection(user_id, reflection_id):
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM reflections WHERE id = %s AND user_id = %s",
        (reflection_id, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_statistics(user_id):
    reflections = get_all_reflections(user_id)

    total_reflections = len(reflections)
    total_messages = sum(len(reflection["messages"]) for reflection in reflections)

    latest_date = "No reflections yet"

    if reflections:
        latest_date = reflections[-1]["date"]

    return {
        "total_reflections": total_reflections,
        "total_messages": total_messages,
        "latest_date": latest_date
    }