from app import app, db
from app.models.models import Book, BookItem, User, Loan
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


@app.post("/loans")
@jwt_required()
def borrow_book():
    user_id = get_jwt_identity()
    data = request.json
    book_id = data["book_id"]
    book_code = data["book_code"]
    book = db.session.query(Book).get(book_id)
    user = db.session.query(User).get(user_id)
    book_item = (
        db.session.query(BookItem)
        .filter_by(book_code=book_code, status="available")
        .first()
    )
    if book and user:
        if book.stock > 0 and book_item:
            if user.count_of_books_borrowed < 3:
                # Create loan
                loan = Loan(
                    user_id=user_id,
                    book_id=book_item.book_id,
                    book_code=book_code,
                    status="borrowed",
                )
                db.session.add(loan)
                # Update value
                book.stock -= 1
                book_item.status = "borrowed"
                user.count_of_books_borrowed += 1
                db.session.commit()
                return jsonify({"message": "Buku berhasil dipinjam"}), 201
            else:
                return jsonify({"message": "Maksimal peminjaman buku adalah 3"}), 400
        else:
            return jsonify({"message": "Buku tidak tersedia"}), 400
    else:
        return jsonify({"message": "Data buku atau user tidak ditemukan"}), 404


@app.put("/loans/<int:loan_id>")
@jwt_required()
def return_book(loan_id):
    loan = db.session.query(Loan).get(loan_id)
    if loan:
        loan.date_of_return = datetime.now().date()
        loan.status = "returned"
        book_item = (
            db.session.query(BookItem)
            .filter_by(book_id=loan.book_id, status="borrowed")
            .first()
        )
        book = db.session.query(Book).get(loan.book_id)
        user = db.session.query(User).get(loan.user_id)
        # Update value
        book_item.status = "available"
        book.stock += 1
        user.count_of_books_borrowed -= 1
        db.session.commit()
        return jsonify({"message": "Buku berhasil dikembalikan"}), 200
    return jsonify({"message": "Data peminjaman tidak ditemukan"}), 404


@app.get("/loans/check/<int:book_id>")
@jwt_required()
def is_book_on_loan(book_id):
    user_id = get_jwt_identity()
    loan = (
        db.session.query(Loan)
        .filter_by(user_id=user_id, book_id=book_id, status="borrowed")
        .first()
    )
    if loan:
        return jsonify({"data": {"is_on_loan": True}}), 200
    return jsonify({"data": {"is_on_loan": False}}), 404


@app.get("/loans/user")
@jwt_required()
def get_user_loans():
    user_id = get_jwt_identity()
    loans = db.session.query(Loan).filter_by(user_id=user_id).all()
    loans_data = []
    for loan in loans:
        book = db.session.query(Book).get(loan.book_id)
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "book_code": loan.book_code,
            "title": book.title,
            "isbn": book.isbn,
            "image_url": book.image_url,
            "loan_date": loan.loan_date,
            "date_of_return": loan.date_of_return,
            "status": loan.status,
        }
        loans_data.append(loan_data)
    return jsonify({"data": loans_data}), 200


@app.get("/loans")
@jwt_required()
def get_loans():
    loans = db.session.query(Loan).all()
    loans_data = []
    for loan in loans:
        book = db.session.query(Book).get(loan.book_id)
        user = db.session.query(User).get(loan.user_id)
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "book_code": loan.book_code,
            "title": book.title,
            "isbn": book.isbn,
            "image_url": book.image_url,
            "loan_date": loan.loan_date,
            "date_of_return": loan.date_of_return,
            "status": loan.status,
            "user_id": loan.user_id,
            "user_name": user.first_name + " " + user.last_name,
        }
        loans_data.append(loan_data)
    return jsonify({"data": loans_data}), 200


@app.get("/loans/<int:loan_id>")
@jwt_required()
def get_loan_by_id(loan_id):
    loan = db.session.query(Loan).get(loan_id)
    if loan:
        book = db.session.query(Book).get(loan.book_id)
        user = db.session.query(User).get(loan.user_id)
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "book_code": loan.book_code,
            "title": book.title,
            "isbn": book.isbn,
            "image_url": book.image_url,
            "loan_date": loan.loan_date,
            "date_of_return": loan.date_of_return,
            "status": loan.status,
            "user_id": loan.user_id,
            "user_name": user.first_name + " " + user.last_name,
        }
        return jsonify({"data": loan_data}), 200
    return jsonify({"message": "Data peminjaman tidak ditemukan"}), 404
