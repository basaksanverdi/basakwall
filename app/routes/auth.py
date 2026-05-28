from flask import (
    request,
    session,
    render_template,
    redirect
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

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

        return redirect("/")


    @app.route("/login", methods=["POST"])
    def login():

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Missing credentials", 400

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "Invalid username or password", 401

        if not check_password_hash(
            user.password_hash,
            password
        ):
            return "Invalid username or password", 401

        session["user_id"] = user.id
        session["username"] = user.username
        print("session:", session)

        # return redirect(f"/profile/{user.username}")
        return redirect("/feed")


    @app.route("/logout")
    def logout():

        session.clear()

        return redirect("/")
