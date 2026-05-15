from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author_endpoint(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_endpoint(
    author_id: int, book: schemas.BookBase, db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.Book])
def get_books_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)


@app.get("/books/by-author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author_endpoint(
    author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db, author_id, skip, limit)
