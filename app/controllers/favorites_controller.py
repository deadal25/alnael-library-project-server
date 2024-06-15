from app import app, db
from app.models.models import Book, User, Favorite
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.post("/favorites")
@jwt_required()
def add_favorite():
    user_id = get_jwt_identity()
    data = request.json
    book_id = data["book_id"]
    user = db.session.query(User).get(user_id)
    book = db.session.query(Book).get(book_id)
    if user and book:
        favorite = Favorite(user_id=user_id, book_id=book_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Buku ditambahkan ke favorit"}), 200
    return jsonify({"message": "Data buku atau user tidak ditemukan"}), 404


@app.get("/favorites")
@jwt_required()
def get_user_favorites():
    user_id = get_jwt_identity()
    favorites = db.session.query(Favorite).filter_by(user_id=user_id).all()
    favorites_data = []
    for favorite in favorites:
        book = db.session.query(Book).get(favorite.book_id)
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
        favorites_data.append(book_data)
    return jsonify({"data": favorites_data}), 200


@app.get("/favorites/<int:book_id>")
@jwt_required()
def is_favorite(book_id):
    user_id = get_jwt_identity()
    favorite = (
        db.session.query(Favorite).filter_by(user_id=user_id, book_id=book_id).first()
    )
    if favorite:
        favorite_data = {
            "id": favorite.id,
            "is_favorite": True,
        }
        return jsonify({"data": favorite_data}), 200
    return jsonify({"data": {"is_favorite": False}}), 404


@app.delete("/favorites/<int:favorite_id>")
@jwt_required()
def remove_favorite(favorite_id):
    user_id = get_jwt_identity()
    favorite = db.session.query(Favorite).get(favorite_id)
    if favorite and favorite.user_id == user_id:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorit berhasil dihapus"}), 200
    return jsonify({"message": "Data favorit tidak ditemukan"}), 404
