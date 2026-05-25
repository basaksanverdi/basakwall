from flask import request
from werkzeug.security import generate_password_hash

from database import db
from app.models.user import User


def register_routes(app):

    @app.route("/register", methods=["POST"])
    def register():

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Missing username or password", 400

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "User already exists", 400

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created successfully", 201
