# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from routes import products
from security import authenticate_user, create_access_token, verify_jwt
from pydantic import BaseModel
from fastapi import APIRouter
import sqlite3
from security import pwd_context

app = FastAPI()

# ------------------- Token Login -------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# ------------------- Admin-only User Creation -------------------
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # "admin", "dev", "user"

@app.post("/users/create")
def create_user(user: UserCreate, current_user: dict = Depends(verify_jwt)):
    # Only admins can create new users
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    hashed_password = pwd_context.hash(user.password)
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Check if username exists
    cursor.execute("SELECT username FROM users WHERE username=?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    # Insert new user
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (user.username, hashed_password, user.role))
    conn.commit()
    conn.close()

    return {"message": f"User {user.username} created successfully with role {user.role}"}

# ------------------- Include Routers -------------------
app.include_router(products.router)
