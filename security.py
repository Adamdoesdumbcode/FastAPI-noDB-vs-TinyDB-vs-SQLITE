# security.py
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import sqlite3

# ------------------- Password Hashing -------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ------------------- JWT Settings -------------------
SECRET_KEY = "d9f3b7e6c4a81f2d9e6b4a7c1f3d8e5b6c9a2f1d4e8b7c3a9d6f2e1b0c8a5f3d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*12

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ------------------- Database helper -------------------
def get_user_from_db(username: str):
    conn = sqlite3.connect("sqlite.db")  # Adjust your DB path
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "hashed_password": row[1], "role": row[2]}
    return None

def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

# ------------------- JWT Helpers -------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_from_db(username)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
