from app import app, db
from app.models.models import User
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.post("/users/sign-up")
def sign_up():
    data = request.json
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data["password"],
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    # Convert the user object to a dictionary
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
    }
    access_token = create_access_token(identity=user.id)
    user_data["access_token"] = access_token
    return jsonify({"user": user_data}), 201


@app.post("/users/sign-in")
def sign_in():
    data = request.json
    user = db.session.query(User).filter_by(email=data["email"]).first()
    if user and user.password == data["password"]:
        access_token = create_access_token(identity=user.id)
        # Convert the user object to a dictionary
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "address": user.address,
            "phone_number": user.phone_number,
            "count_of_books_borrowed": user.count_of_books_borrowed,
            "role": user.role,
            "access_token": access_token,
        }
        return jsonify({"user": user_data}), 200
    return jsonify({"message": "Email atau password salah."}), 401


@app.get("/users/profile")
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).get(current_user_id)
    # Convert the user object to a dictionary
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
        "phone_number": user.phone_number,
        "count_of_books_borrowed": user.count_of_books_borrowed,
        "role": user.role,
    }
    return jsonify({"user": user_data}), 200


@app.put("/users/profile")
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = db.session.query(User).get(current_user_id)
    data = request.json
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.age = data["age"]
    user.address = data["address"]
    user.phone_number = data["phone_number"]
    db.session.commit()
    # Convert the user object to a dictionary
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
        "phone_number": user.phone_number,
        "role": user.role,
    }
    return jsonify({"user": user_data, "message": "Profil berhasil diperbarui."}), 200
