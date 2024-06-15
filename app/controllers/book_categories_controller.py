from app import app, db
from app.models.models import Category
from flask import jsonify


@app.get("/books/categories")
def get_book_categories():
    categories = db.session.query(Category).all()
    categories_data = []
    for category in categories:
        category_data = {
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }
        categories_data.append(category_data)
    return jsonify({"data": categories_data}), 200
