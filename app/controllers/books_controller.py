from app import app, db
from app.models.models import (
    Book,
    BookItem,
    BookCategory,
    Category,
    Loan,
    Favorite,
    Review,
)
from flask import request, jsonify
from flask_jwt_extended import jwt_required


@app.post("/books")
@jwt_required()
def add_book():
    data = request.json
    book = Book(
        isbn=data["isbn"],
        title=data["title"],
        image_url=data["image_url"],
        author=data["author"],
        publisher=data["publisher"],
        publication_year=data["publication_year"],
        description=data["description"],
        stock=data["stock"],
    )
    db.session.add(book)
    db.session.flush()
    book_category_ids = []
    for category_id in data["category_ids"]:
        book_category = BookCategory(book_id=book.id, category_id=category_id)
        book_category_ids.append(book_category)
    db.session.bulk_save_objects(book_category_ids)
    book_items = []
    for i in range(data["stock"]):
        book_item = BookItem(book_id=book.id, book_code=f"{book.isbn}-{i}")
        book_items.append(book_item)
    db.session.bulk_save_objects(book_items)
    db.session.commit()
    book_data = {
        "id": book.id,
        "isbn": book.isbn,
        "title": book.title,
        "image_url": book.image_url,
        "author": book.author,
        "publisher": book.publisher,
        "publication_year": book.publication_year,
        "description": book.description,
        "stock": book.stock,
    }
    return jsonify({"book": book_data}), 201


@app.get("/books")
def get_books():
    books = db.session.query(Book).all()
    books_data = []
    for book in books:
        categories = []
        book_categories = (
            db.session.query(BookCategory).filter_by(book_id=book.id).all()
        )
        for book_category in book_categories:
            category = db.session.query(Category).get(book_category.category_id)
            categories.append(category.name)
        book_data = {
            "id": book.id,
            "isbn": book.isbn,
            "title": book.title,
            "image_url": book.image_url,
            "author": book.author,
            "publisher": book.publisher,
            "publication_year": book.publication_year,
            "description": book.description,
            "stock": book.stock,
            "categories": categories,
        }
        books_data.append(book_data)
    return jsonify({"data": books_data}), 200


@app.get("/books/<int:book_id>")
def get_book_by_id(book_id):
    book = db.session.query(Book).get(book_id)
    if book:
        categories = []
        book_categories = (
            db.session.query(BookCategory).filter_by(book_id=book.id).all()
        )
        for book_category in book_categories:
            category = db.session.query(Category).get(book_category.category_id)
            category_data = {"id": category.id, "name": category.name}
            categories.append(category_data)
        book_data = {
            "id": book.id,
            "isbn": book.isbn,
            "title": book.title,
            "image_url": book.image_url,
            "author": book.author,
            "publisher": book.publisher,
            "publication_year": book.publication_year,
            "description": book.description,
            "stock": book.stock,
            "categories": categories,
        }
        return jsonify({"data": book_data}), 200
    return jsonify({"message": "Buku tidak ditemukan."}), 404


@app.put("/books/<int:book_id>")
@jwt_required()
def update_book(book_id):
    data = request.json
    book = db.session.query(Book).get(book_id)
    book.isbn = data["isbn"]
    book.title = data["title"]
    book.image_url = data["image_url"]
    book.author = data["author"]
    book.publisher = data["publisher"]
    book.publication_year = data["publication_year"]
    book.description = data["description"]
    book.stock = data["stock"]
    # Delete all book categories, then add new book categories
    db.session.query(BookCategory).filter_by(book_id=book_id).delete()
    book_category_ids = []
    for category_id in data["category_ids"]:
        book_category = BookCategory(book_id=book_id, category_id=category_id)
        book_category_ids.append(book_category)
    db.session.bulk_save_objects(book_category_ids)
    db.session.commit()
    book_data = {
        "id": book.id,
        "isbn": book.isbn,
        "title": book.title,
        "image_url": book.image_url,
        "author": book.author,
        "publisher": book.publisher,
        "publication_year": book.publication_year,
        "description": book.description,
        "stock": book.stock,
    }
    return jsonify({"data": book_data}), 200


@app.delete("/books/<int:book_id>")
@jwt_required()
def delete_book(book_id):
    loan = db.session.query(Loan).filter_by(book_id=book_id, status="borrowed").first()
    if loan:
        return (
            jsonify({"message": "Tidak dapat menghapus buku yang sedang dipinjam."}),
            400,
        )
    book = db.session.query(Book).get(book_id)
    if not book:
        return jsonify({"message": "Buku tidak ditemukan."}), 404
    db.session.query(BookCategory).filter_by(book_id=book_id).delete()
    db.session.query(BookItem).filter_by(book_id=book_id).delete()
    db.session.query(Loan).filter_by(book_id=book_id).delete()
    db.session.query(Favorite).filter_by(book_id=book_id).delete()
    db.session.query(Review).filter_by(book_id=book_id).delete()
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Buku berhasil dihapus."}), 200


@app.get("/books/<int:book_id>/book-items")
def get_book_items_by_book_id(book_id):
    book_items = db.session.query(BookItem).filter_by(book_id=book_id).all()
    book_items_data = []
    for book_item in book_items:
        book_item_data = {
            "id": book_item.id,
            "book_code": book_item.book_code,
            "status": book_item.status,
        }
        book_items_data.append(book_item_data)
    return jsonify({"data": book_items_data}), 200
