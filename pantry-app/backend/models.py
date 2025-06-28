from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

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