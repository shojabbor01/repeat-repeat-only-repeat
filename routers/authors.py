from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud

router = APIRouter(prefix="/authors", tags=["authors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Authorout)
def create_author(author: schemas.Authorcreate, db: Session = Depends(get_db)):
    if db.query(crud.models.Author).filter_by(name=author.name).first():
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)

@router.get("/", response_model=list[schemas.Authorout])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@router.get("/{author_id}", response_model=schemas.Authoroutwithbooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=schemas.Authorout)
def update_author(author_id: int, author_in: schemas.Authorcreate, db: Session = Depends(get_db)):
    updated = crud.update_author(db, author_id, author_in.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated

@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_author(db, author_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"detail": "Author deleted"}
