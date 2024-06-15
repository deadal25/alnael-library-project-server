from app import app, db
from app.models.models import Book, User, Review
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.post("/reviews")
@jwt_required()
def add_review():
    user_id = get_jwt_identity()
    data = request.json
    book_id = data["book_id"]
    review_comment = data["review_comment"]
    user = db.session.query(User).get(user_id)
    book = db.session.query(Book).get(book_id)
    if user and book:
        review = Review(user_id=user_id, book_id=book_id, review_comment=review_comment)
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Review berhasil ditambahkan"}), 200
    return jsonify({"message": "Data buku atau user tidak ditemukan"}), 404


@app.get("/reviews/<int:book_id>")
def get_reviews_by_book_id(book_id):
    reviews = db.session.query(Review).filter_by(book_id=book_id).all()
    reviews_data = []
    for review in reviews:
        user = db.session.query(User).get(review.user_id)
        review_data = {
            "id": review.id,
            "user_id": review.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "review_comment": review.review_comment,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        reviews_data.append(review_data)
    return jsonify({"data": reviews_data}), 200


@app.delete("/reviews/<int:review_id>")
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = db.session.query(Review).get(review_id)
    if review and review.user_id == user_id:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review berhasil dihapus"}), 200
    return jsonify({"message": "Data review tidak ditemukan"}), 404


@app.get("/reviews/user")
@jwt_required()
def get_user_reviews():
    user_id = get_jwt_identity()
    reviews = db.session.query(Review).filter_by(user_id=user_id).all()
    reviews_data = []
    for review in reviews:
        book = db.session.query(Book).get(review.book_id)
        review_data = {
            "id": review.id,
            "book_id": review.book_id,
            "title": book.title,
            "image_url": book.image_url,
            "review_comment": review.review_comment,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        reviews_data.append(review_data)
    return jsonify({"data": reviews_data}), 200
