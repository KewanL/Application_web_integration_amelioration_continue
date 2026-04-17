import sqlite3
import os

DB_PATH = os.path.join("database", "cine.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Supprimer tables si existent
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS members")
    cursor.execute("DROP TABLE IF EXISTS films")

    # Tables
    cursor.execute("""
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        film_id INTEGER,
        FOREIGN KEY(member_id) REFERENCES members(id),
        FOREIGN KEY(film_id) REFERENCES films(id)
    )
    """)

    # Données test
    cursor.execute("INSERT INTO members (name, balance) VALUES ('Alice', 50)")
    cursor.execute("INSERT INTO members (name, balance) VALUES ('Bob', 10)")

    cursor.execute("INSERT INTO films (title, price) VALUES ('Inception', 15)")
    cursor.execute("INSERT INTO films (title, price) VALUES ('Matrix', 12)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de données initialisée.")