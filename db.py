import sqlite3

conn = sqlite3.connect("products.db", check_same_thread=False)
c = conn.cursor()

# create table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    stock INTEGER
)""")
conn.commit()
