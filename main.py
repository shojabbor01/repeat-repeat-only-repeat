from fastapi import FastAPI
from database import engine
import models
from routers import authors, books

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API (без пользователей)")

app.include_router(authors.router)
app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Library API bez polzovateley toghe rabotaet"}
