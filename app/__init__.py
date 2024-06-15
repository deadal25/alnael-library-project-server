from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = "secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/db_alnael_library"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

CORS(app)


# Custom JWT's Error Messages
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"message": "Akses gagal. Harap berikan token yang valid."}), 401


@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({"message": "Token telah kedaluwarsa. Silakan login ulang."}), 401


from app.controllers import (
    users_controller,
    books_controller,
    favorites_controller,
    loans_controller,
    reviews_controller,
    book_categories_controller,
)
