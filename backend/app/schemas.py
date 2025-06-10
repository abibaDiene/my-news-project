from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class ReadingStatus(str, Enum):
    TO_READ = "to_read"
    READING = "reading"
    READ = "read"

# Schémas pour l'authentification
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schémas pour les livres
class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    reading_status: ReadingStatus = ReadingStatus.TO_READ

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    reading_status: Optional[ReadingStatus] = None

class Book(BookBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BookList(BaseModel):
    books: List[Book]
    total: int