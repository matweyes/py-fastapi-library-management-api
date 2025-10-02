from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


# Author CRUD operations
def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    """Create a new author in the database."""
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
    """Retrieve a paginated list of authors."""
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    """Retrieve a single author by ID."""
    return db.query(models.Author).filter(models.Author.id == author_id).first()


# Book CRUD operations
def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    """Create a new book for a specific author."""
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = None
) -> list[models.Book]:
    """
    Retrieve a paginated list of books.
    Optionally filter by author_id.
    """
    query = db.query(models.Book)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10) -> list[models.Book]:
    """Retrieve books filtered by a specific author ID."""
    return db.query(models.Book).filter(
        models.Book.author_id == author_id
    ).offset(skip).limit(limit).all()