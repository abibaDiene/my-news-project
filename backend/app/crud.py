from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from app.auth import get_password_hash
from typing import List, Optional

# CRUD pour les utilisateurs
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD pour les livres
def get_books(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(
        models.Book.owner_id == user_id
    ).offset(skip).limit(limit).all()

def get_books_count(db: Session, user_id: int):
    return db.query(func.count(models.Book.id)).filter(
        models.Book.owner_id == user_id
    ).scalar()

def get_book(db: Session, book_id: int, user_id: int):
    return db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user_id
    ).first()

def create_book(db: Session, book: schemas.BookCreate, user_id: int):
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate, user_id: int):
    db_book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user_id
    ).first()
    
    if db_book:
        update_data = book_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
    
    return db_book

def delete_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == user_id
    ).first()
    
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def search_books(db: Session, user_id: int, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(
        models.Book.owner_id == user_id,
        models.Book.title.contains(query) | models.Book.author.contains(query)
    ).offset(skip).limit(limit).all()