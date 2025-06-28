from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from dotenv import load_dotenv
from ..models import User, UserCreate, UserLogin, UserResponse  # Relative import within backend package
from ..main import app  # Relative import within backend package

# Security models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

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
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise HTTPException(status_code=500, detail="Secret key not configured")
    return jwt.encode(to_encode, secret_key, algorithm="HS256")

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise HTTPException(status_code=500, detail="Secret key not configured")
    return jwt.encode(data, secret_key, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise HTTPException(status_code=500, detail="Secret key not configured")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username = payload.get("sub")
        if not isinstance(username, str):
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    from ..models.user import User  # Relative import within backend package
    cursor = app.state.db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (token_data.username,))
    user = cursor.fetchone()
    if not user:
        raise credentials_exception
    return User(*user)

# Authentication routes
from fastapi import APIRouter
from ..models import UserCreate, UserLogin, UserResponse  # Correct relative import from backend.models

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    from ..models.user import User  # Relative import within backend package
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

@router.post("/token", response_model=Token)
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
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user[1]}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user[1]})
    
    cursor.execute("UPDATE users SET refresh_token = ? WHERE id = ?", (refresh_token, user[0]))
    app.state.db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh-token", response_model=Token)
def refresh_token(refresh_token: str):
    cursor = app.state.db.cursor()  # Ensure app import is already present
    cursor.execute("SELECT * FROM users WHERE refresh_token = ?", (refresh_token,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    try:
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise HTTPException(status_code=500, detail="Secret key not configured")
        payload = jwt.decode(refresh_token, secret_key, algorithms=["HS256"])
        username = payload.get("sub")
        if not isinstance(username, str):
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if not isinstance(username, str):
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    cursor.execute("UPDATE users SET refresh_token = ? WHERE id = ?", (new_refresh_token, user[0]))
    app.state.db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }