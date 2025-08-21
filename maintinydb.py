from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB, Query

# Database
db = TinyDB("products.json")
ProductQuery = Query()

app = FastAPI()

# Product schema
class Product(BaseModel):
    name: str
    price: int
    stock: int

# Read all products
@app.get("/items")
def read_items():
    return db.all()

# Read single product
@app.get("/item/{id}")
def read_item(id: int):
    product = db.get(doc_id=id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product id {id} not found")
    return product

# Add product
@app.post("/add")
def add(product: Product):
    doc_id = db.insert(product.dict())
    return {
        "message": f"Added {product.name} with id {doc_id}",
        "products": db.all()
    }

# Remove product
@app.delete("/remove/{id}")
def remove(id: int):
    if not db.contains(doc_id=id):
        raise HTTPException(status_code=404, detail=f"No such product id {id}")
    db.remove(doc_ids=[id])
    return {"message": f"Removed product id {id}"}

# Replace product
@app.put("/replace/{id}")
def replace(id: int, product: Product):
    if not db.contains(doc_id=id):
        raise HTTPException(status_code=404, detail=f"No such product id {id}")
    db.update(product.dict(), doc_ids=[id])
    return {"message": f"Replaced product id {id}"}

# Search product by name
@app.get("/search/{search}")
def search(search: str):
    result = db.search(ProductQuery.name.matches(search, flags="i"))
    if not result:
        return {"error": "No matching products found"}
    return result
