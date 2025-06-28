from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection
    app.state.db = sqlite3.connect("pantry.db")
    try:
        yield
    finally:
        app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Allow CORS for Expo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:19006"],  # Default Expo development client port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pantry App Backend is Running", "status": "healthy"}

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# User models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class PantryItemCreate(BaseModel):
    name: str
    quantity: int
    category: str
    expiration_date: str

class PantryItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    category: str
    expiration_date: str
    user_id: int

# Token models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Database models
class User:
    def __init__(self, id, username, email, hashed_password, refresh_token):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.refresh_token = refresh_token

class PantryItem:
    def __init__(self, id, name, quantity, category, expiration_date, user_id):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.category = category
        self.expiration_date = expiration_date
        self.user_id = user_id

# Security utilities
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (token_data.username,))
    user = cursor.fetchone()
    if not user:
        raise credentials_exception
    return User(*user)

# Database initialization
@app.on_event("startup")
def create_tables():
    cursor = app.state.db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        refresh_token TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pantry_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT,
        expiration_date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    app.state.db.commit()

# Authentication routes
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (user.username, user.email))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = get_password_hash(user.password)
    refresh_token = create_refresh_token({"sub": user.username})
    
    cursor.execute("""
    INSERT INTO users (username, email, hashed_password, refresh_token)
    VALUES (?, ?, ?, ?)
    """, (user.username, user.email, hashed_password, refresh_token))
    app.state.db.commit()
    
    return {"id": cursor.lastrowid, "username": user.username, "email": user.email}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    user = cursor.fetchone()
    if not user or not verify_password(form_data.password, user[3]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[1]}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user[1]})
    
    # Update user's refresh token
    cursor.execute("UPDATE users SET refresh_token = ? WHERE id = ?", (refresh_token, user[0]))
    app.state.db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh-token", response_model=Token)
def refresh_token(refresh_token: str):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM users WHERE refresh_token = ?", (refresh_token,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    # Update user's refresh token
    cursor.execute("UPDATE users SET refresh_token = ? WHERE id = ?", (new_refresh_token, user[0]))
    app.state.db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Pantry item CRUD routes
@app.post("/pantry-items", response_model=PantryItemResponse)
def create_pantry_item(item: PantryItemCreate, current_user: User = Depends(get_current_user)):
    cursor = app.state.db.cursor()
    cursor.execute("""
    INSERT INTO pantry_items (name, quantity, category, expiration_date, user_id)
    VALUES (?, ?, ?, ?, ?)
    """, (item.name, item.quantity, item.category, item.expiration_date, current_user.id))
    app.state.db.commit()
    return {
        "id": cursor.lastrowid,
        "name": item.name,
        "quantity": item.quantity,
        "category": item.category,
        "expiration_date": item.expiration_date,
        "user_id": current_user.id
    }

@app.get("/pantry-items/{item_id}", response_model=PantryItemResponse)
def read_pantry_item(item_id: int, current_user: User = Depends(get_current_user)):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM pantry_items WHERE id = ? AND user_id = ?", (item_id, current_user.id))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not owned by user")
    return {
        "id": item[0],
        "name": item[1],
        "quantity": item[2],
        "category": item[3],
        "expiration_date": item[4],
        "user_id": item[5]
    }

@app.put("/pantry-items/{item_id}", response_model=PantryItemResponse)
def update_pantry_item(item_id: int, item: PantryItemCreate, current_user: User = Depends(get_current_user)):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM pantry_items WHERE id = ? AND user_id = ?", (item_id, current_user.id))
    existing_item = cursor.fetchone()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found or not owned by user")
    
    cursor.execute("""
    UPDATE pantry_items
    SET name = ?, quantity = ?, category = ?, expiration_date = ?
    WHERE id = ? AND user_id = ?
    """, (item.name, item.quantity, item.category, item.expiration_date, item_id, current_user.id))
    app.state.db.commit()
    
    cursor.execute("SELECT * FROM pantry_items WHERE id = ? AND user_id = ?", (item_id, current_user.id))
    updated_item = cursor.fetchone()
    return {
        "id": updated_item[0],
        "name": updated_item[1],
        "quantity": updated_item[2],
        "category": updated_item[3],
        "expiration_date": updated_item[4],
        "user_id": updated_item[5]
    }

@app.delete("/pantry-items/{item_id}", response_model=dict)
def delete_pantry_item(item_id: int, current_user: User = Depends(get_current_user)):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM pantry_items WHERE id = ? AND user_id = ?", (item_id, current_user.id))
    item = cursor.fetchone()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not owned by user")
    
    cursor.execute("DELETE FROM pantry_items WHERE id = ? AND user_id = ?", (item_id, current_user.id))
    app.state.db.commit()
    
    return {"message": "Item deleted successfully", "item_id": item_id}
@app.get("/pantry-items", response_model=list[PantryItemResponse])
def list_pantry_items(current_user: User = Depends(get_current_user)):
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM pantry_items WHERE user_id = ?", (current_user.id,))
    items = cursor.fetchall()
    return [
        PantryItemResponse(
            id=item[0],
            name=item[1],
            quantity=item[2],
            category=item[3],
            expiration_date=item[4],
            user_id=item[5]
        ) for item in items
    ]