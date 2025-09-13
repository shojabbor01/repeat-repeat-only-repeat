from pydantic import BaseModel
from typing import List, Optional

class Authorcreate(BaseModel):
    name: str
    
    
class Bookoutsimple(BaseModel):
    id: int
    title: str
    year: int
    available: int
    
    class Config:
        from_atributes = True
        
class Authorout(BaseModel):
    id: int
    name: str
    class Config:
        from_atributes = True
        
        
class Authoroutwithbooks(BaseModel):
    id: int
    name: str
    books: List[Bookoutsimple] = []
    
    class Config:
        from_atributes = True
        
        
class Bookcreate(BaseModel):
    title: str
    year: int
    author_id: int
    available: Optional[int]=1
    
    
class Bookout(BaseModel):
    id: int
    title: str
    year: int
    available: int
    author: Authorout
    
    class Config:
        from_atributes = True
        
        