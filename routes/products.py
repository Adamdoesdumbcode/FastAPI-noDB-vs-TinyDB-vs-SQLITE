
from fastapi import APIRouter, Depends, HTTPException

from crud import reset_db
from schemas import Product
import crud
from security import get_api_key, get_dev_key


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_items(api_key: str = Depends(get_api_key)):
   return crud.get_items()

@router.get("/{id}")
def get_item(id: int, api_key: str = Depends(get_api_key)):
   return crud.get_item(id)

@router.post("/")
def add_item(item: Product, api_key: str = Depends(get_api_key)):
    return crud.add_item(item)

@router.delete("/{id}")
def delete_item(id: int, api_key: str = Depends(get_api_key)):
    return crud.delete_item(id)

@router.put("/{id}")
def update_item(id: int, item: Product, api_key: str = Depends(get_api_key)):
    return crud.update_item(id, item)

@router.get("/search/{search}")
def search_item(search: str, api_key: str = Depends(get_api_key)):
    results = crud.search_items(search)
    if not results:
        return {"Message": "No products found"}
    return results

@router.delete("/dbwipe")
def dbwipe(dev_key: str = Depends(get_dev_key)):
    return reset_db()


