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

from datetime import datetime
from zoneinfo import ZoneInfo

from database import db
from app.models.user import User
from app.models.login_history import LoginHistory


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

        if "user_id" in session:

            old_user = User.query.get(
                session["user_id"]
            )

            if old_user:

                old_user.is_online = False

                old_user.last_seen = datetime.now(
                    ZoneInfo("Europe/Istanbul")
                )

                active_session = LoginHistory.query.filter_by(
                    user_id=old_user.id,
                    logout_time=None
                ).order_by(
                    LoginHistory.login_time.desc()
                ).first()

                if active_session:

                    active_session.logout_time = datetime.now(
                        ZoneInfo("Europe/Istanbul")
                    )

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

        user.is_online = True

        new_login = LoginHistory(
            user_id=user.id,
            ip_address=request.remote_addr
        )

        db.session.add(new_login)

        db.session.commit()

        session["user_id"] = user.id
        session["username"] = user.username

        print("session:", session)

        return redirect("/feed")


    @app.route("/logout")
    def logout():

        if "user_id" in session:

            user = User.query.get(
                session["user_id"]
            )

            if user:

                user.is_online = False

                user.last_seen = datetime.now(
                    ZoneInfo("Europe/Istanbul")
                )

                active_session = LoginHistory.query.filter_by(
                    user_id=user.id,
                    logout_time=None
                ).order_by(
                    LoginHistory.login_time.desc()
                ).first()

                if active_session:

                    active_session.logout_time = datetime.now(
                        ZoneInfo("Europe/Istanbul")
                    )

                db.session.commit()

        session.clear()

        return redirect("/")