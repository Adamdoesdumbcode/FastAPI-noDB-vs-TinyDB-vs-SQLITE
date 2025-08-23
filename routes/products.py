from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from crud import reset_db
from schemas import Product
import crud
from security import verify_jwt, authenticate_user, create_access_token  # new JWT dependency

router = APIRouter(prefix="/products", tags=["Products"])
app = FastAPI()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# ---- JWT-protected endpoints ----
@router.get("/")
def get_items(current_user: dict = Depends(verify_jwt)):
    return crud.get_items()

@router.get("/{id}")
def get_item(id: int, current_user: dict = Depends(verify_jwt)):
    return crud.get_item(id)

@router.post("/")
def add_item(item: Product, current_user: dict = Depends(verify_jwt)):
    return crud.add_item(item)

@router.delete("/{id}")
def delete_item(id: int, current_user: dict = Depends(verify_jwt)):
    return crud.delete_item(id)

@router.put("/{id}")
def update_item(id: int, item: Product, current_user: dict = Depends(verify_jwt)):
    return crud.update_item(id, item)

@router.get("/search/{search}")
def search_item(search: str, current_user: dict = Depends(verify_jwt)):
    results = crud.search_items(search)
    if not results:
        return {"Message": "No products found"}
    return results

# ---- JWT-protected dev-only endpoint ----
@router.post("/dbwipe")
def dbwipe(current_user: dict = Depends(verify_jwt)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    return reset_db()
