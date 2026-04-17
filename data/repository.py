import sqlite3
import os

DB_PATH = os.path.join("database", "cine.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


# ---- FILMS ----
def add_film(title, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO films (title, price) VALUES (?, ?)", (title, price))
    conn.commit()
    conn.close()


def get_films():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films")
    films = cursor.fetchall()
    conn.close()
    return films


# ---- MEMBERS ----
def add_member(name, balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    conn.close()


def get_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return members


def update_balance(member_id, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET balance = ? WHERE id = ?", (new_balance, member_id))
    conn.commit()
    conn.close()


# ---- TRANSACTIONS ----
def add_transaction(member_id, film_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (member_id, film_id) VALUES (?, ?)", (member_id, film_id))
    conn.commit()
    conn.close()


def get_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    return member


def get_film(film_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films WHERE id = ?", (film_id,))
    film = cursor.fetchone()
    conn.close()
    return film