from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
    
    
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    available = Column(Integer, default=1)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    author = relationship("Author", back_populates="books")
    
    
    