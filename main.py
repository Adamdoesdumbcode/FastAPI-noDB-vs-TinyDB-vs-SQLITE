from itertools import product
from typing import Union
import random
from fastapi import FastAPI
from pydantic import BaseModel
import json
from tinydb import TinyDB, Query
db = TinyDB("products.json")
app = FastAPI()

products = {
    1: {"name": "shirt", "price": 20, "stock": 50},
    2: {"name": "pants", "price": 23, "stock": 40},
}


@app.get("/item/{id}")
def read_item(id: int):
    return products[id]

@app.get("/items")
def read_items():
    return products

class Product(BaseModel):
    name: str
    price: int
    stock: int

@app.post("/add")
def add(product: Product):
    newid = max(products.keys(), default=0) + 1
    products[newid] = product.dict()
    return {
        "message": f"you have added {product.name} with id {newid}. this is the full list of products now.",
        "products": products
    }

@app.post("/remove/{id}")
def remove(id: int):
    if id in products:
        del products[id]
        return {
            "message": f"you removed product id {id}"
        }
    else:
        return {"message": f"no such product id {id}"}



@app.put("/replace/{id}")
def replace(id: int, product: Product):
    if id in products:
        products[id] = product.dict()
    else:
        return {"message": f"no such product id {id}"}


@app.get("/search/{search}")
def search(search: str):
    for pid, product in products.items():
        if product["name"].lower() == search.lower():
            return product
    return {"error": "this is not a valid product"}

