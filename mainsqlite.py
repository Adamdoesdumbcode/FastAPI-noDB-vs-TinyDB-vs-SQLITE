from typing import Union
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import sqlite3
import secrets

# --- Generate API key ---
API_KEY = f"STAMI_{secrets.token_urlsafe(16)}"
print(f"Your new API key is: {API_KEY}")

app = FastAPI()

# --- SQLite setup ---
conn = sqlite3.connect("products.db", check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    stock INTEGER
)""")
conn.commit()

# --- Pydantic model ---
class Product(BaseModel):
    name: str
    price: int
    stock: int

# --- API Key dependency ---
api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

# --- API routes ---
@app.get("/item/{id}")
def read_item(id: int, api_key: str = Depends(get_api_key)):
    c.execute("""SELECT * FROM products WHERE id = ?""" , (id,))
    rows = c.fetchone()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]

@app.get("/items")
def read_items(api_key: str = Depends(get_api_key)):
    c.execute("SELECT * FROM products")
    rows =  c.fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]

@app.post("/add")
def add(product: Product, api_key: str = Depends(get_api_key)):
    c.execute("""INSERT INTO products (name, price, stock) VALUES (?, ?, ?)""", (product.name, product.price, product.stock))
    conn.commit()

@app.delete("/remove/{id}")
def remove(id: int, api_key: str = Depends(get_api_key)):
    c.execute("""DELETE FROM products WHERE id = ?""", (id,))
    conn.commit()

@app.put("/replace/{id}")
def replace(id: int, product: Product, api_key: str = Depends(get_api_key)):
    c.execute("""UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?""", (product.name, product.price, product.stock, id))
    conn.commit()

@app.get("/search/{search}")
def search(search: str, api_key: str = Depends(get_api_key)):
    search_term = f"%{search}%"
    c.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", (search_term,))
    rows = c.fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]
