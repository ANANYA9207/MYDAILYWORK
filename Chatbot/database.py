import sqlite3
import json

def setup_database():
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS intents(
        intent TEXT,
        pattern TEXT,
        response TEXT
    )
    """)
    conn.commit()

    with open('intents.json') as f:
        data = json.load(f)

    cur.execute("DELETE FROM intents")  # avoid duplicates

    for intent, details in data.items():
        for pattern in details["patterns"]:
            for response in details["responses"]:
                cur.execute(
                    "INSERT INTO intents VALUES (?, ?, ?)",
                    (intent, pattern, response)
                )

    conn.commit()
    conn.close()
