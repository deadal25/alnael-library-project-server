from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    age = Column(Integer)
    address = Column(Text)
    phone_number = Column(String(15))
    count_of_books_borrowed = Column(Integer, default=0)
    role = Column(Enum("admin", "user"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)


class Book(Base):
    __tablename__ = "books"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    isbn = Column(String(255), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    image_url = Column(String(255))
    author = Column(String(255), nullable=False)
    publisher = Column(String(255))
    publication_year = Column(Integer)
    description = Column(Text)
    stock = Column(Integer, nullable=False)


class BookItem(Base):
    __tablename__ = "book_items"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book_code = Column(String(255), nullable=False, unique=True)
    status = Column(
        Enum("available", "borrowed"),
        default="available",
        nullable=False,
    )


class Category(Base):
    __tablename__ = "categories"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)


class BookCategory(Base):
    __tablename__ = "books_categories"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)


class Loan(Base):
    __tablename__ = "loans"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book_code = Column(String(255), nullable=False)
    loan_date = Column(Date, default=datetime.now)
    date_of_return = Column(Date)
    status = Column(Enum("borrowed", "returned"), nullable=False)


class Review(Base):
    __tablename__ = "reviews"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    review_comment = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)


class Favorite(Base):
    __tablename__ = "favorites"
    # Attributes
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
