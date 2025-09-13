from sqlalchemy.orm import Session
import models, schemas

def create_author(db: Session, author: schemas.Authorcreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def update_author(db: Session, author_id: int, name: str):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    db_author.name = name
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if not db_author:
        return False
    db.delete(db_author)
    db.commit()
    return True

def create_book(db: Session, book: schemas.Bookcreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, author_id: int | None = None, year: int | None = None, skip: int = 0, limit: int = 100):
    q = db.query(models.Book)
    if author_id is not None:
        q = q.filter(models.Book.author_id == author_id)
    if year is not None:
        q = q.filter(models.Book.year == year)
    return q.offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book_in: schemas.Bookcreate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    for key, value in book_in.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
