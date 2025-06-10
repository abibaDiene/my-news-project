from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import schemas, crud
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=schemas.BookList)
async def read_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search in title and author"),
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir la liste des livres de l'utilisateur"""
    
    if search:
        books = crud.search_books(db, user_id=current_user.id, query=search, skip=skip, limit=limit)
        # Pour la recherche, on compte tous les résultats trouvés
        total = len(crud.search_books(db, user_id=current_user.id, query=search, skip=0, limit=1000))
    else:
        books = crud.get_books(db, user_id=current_user.id, skip=skip, limit=limit)
        total = crud.get_books_count(db, user_id=current_user.id)
    
    return {"books": books, "total": total}

@router.post("/", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer un nouveau livre"""
    return crud.create_book(db=db, book=book, user_id=current_user.id)

@router.get("/{book_id}", response_model=schemas.Book)
async def read_book(
    book_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtenir un livre spécifique"""
    book = crud.get_book(db, book_id=book_id, user_id=current_user.id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un livre"""
    book = crud.update_book(db, book_id=book_id, book_update=book_update, user_id=current_user.id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un livre"""
    success = crud.delete_book(db, book_id=book_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
