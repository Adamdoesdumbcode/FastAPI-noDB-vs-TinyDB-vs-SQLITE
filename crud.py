from datetime import datetime

from db import c, conn
from schemas import Product


# crud.py

def get_item(id: int):
    c.execute("SELECT * FROM products WHERE id = ?", (id,))
    rows = c.fetchone()
    r = rows
    if not r:
        return {"Message": "Item not found"}
    return {"id": r[0], "name": r[1], "price": r[2], "stock": r[3]}


def get_items():
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]


def add_item(item: Product):
    c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (item.name, item.price, item.stock))
    conn.commit()
    return {
        "Message": "Item added",
        "id": c.lastrowid,
        "name": item.name,
        "price": item.price,
        "stock": item.stock,
        "date": datetime.now().isoformat()
    }


def delete_item(id: int):
    c.execute(
        "DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    if c.rowcount == 0:
        return {"Message": f"No product found with id {id}"}
    return {
        "Message": "Item deleted",
    }

def update_item(id: int, item: Product):
    c.execute("UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?", (item.name, item.price, item.stock, id))
    conn.commit()
    if c.rowcount == 0:
        return {"Message": f"No product found with id {id}"}
    return {
        "Message": "Item updated",
    }


def search_items(search: str):
    search_term = f"%{search}%"
    c.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", (search_term,))
    rows = c.fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]


def reset_db():
    c.execute("DELETE FROM products")                  # remove all rows
    c.execute("DELETE FROM sqlite_sequence WHERE name='products'")  # reset autoincrement
    conn.commit()
    return {"Message": "Database reset"}




