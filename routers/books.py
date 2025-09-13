from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from database import SessionLocal
import schemas, crud, models

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Bookout)
def create_book(book: schemas.Bookcreate, db: Session = Depends(get_db)):
    if not crud.get_author(db, book.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.Bookout])
def list_books(
    author_id: int | None = Query(None, description="ID avtora dlya fitracii"),
    year: int | None = Query(None, description="god vipuska knigi"),
    available: int | None = Query(None, description="filtr po dostupnosti (1 ili 0)"),
    sort_by: str = Query("title", description="pole dlya sortirovki: title, year ili available"),
    order: str = Query("asc", description="poryadok sortirovki: asc ili desc"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):

    query = db.query(models.Book)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    if year is not None:
        query = query.filter(models.Book.year == year)
    if available is not None:
        query = query.filter(models.Book.available == available)


    valid_fields = {"title": models.Book.title, "year": models.Book.year, "available": models.Book.available}
    sort_field = valid_fields.get(sort_by, models.Book.title)
    query = query.order_by(asc(sort_field) if order == "asc" else desc(sort_field))

    return query.offset(skip).limit(limit).all()

@router.get("/{book_id}", response_model=schemas.Bookout)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.Bookout)
def update_book(book_id: int, book_in: schemas.Bookcreate, db: Session = Depends(get_db)):
    if not crud.get_author(db, book_in.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    updated = crud.update_book(db, book_id, book_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
