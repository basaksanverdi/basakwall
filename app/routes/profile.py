from flask import render_template, session
from app.models.user import User


def register_profile_routes(app):

    @app.route("/profile/<username>")
    def user_profile(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        print(session)

        return render_template(
            "profile.html",
            user=user,
            current_user=session["username"]
        )