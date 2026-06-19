from flask import session, redirect, request
from app.models.follow import Follow
from app.models.user import User
from database import db
from app.routes.notifications import create_notification, delete_notification


def register_follow_routes(app):

    @app.route("/follow/<username>")
    def follow_user(username):

        if "user_id" not in session:
            return "Unauthorized", 401

        user_to_follow = User.query.filter_by(
            username=username
        ).first()

        if not user_to_follow:
            return "User not found"

        existing_follow = Follow.query.filter_by(
            follower_id=session["user_id"],
            following_id=user_to_follow.id
        ).first()

        if existing_follow:
            return redirect(request.referrer)

        follow = Follow(
            follower_id=session["user_id"],
            following_id=user_to_follow.id
        )

        db.session.add(follow)

        current_user = User.query.get(session["user_id"])

        create_notification(
            user_id=user_to_follow.id,
            actor_id=session["user_id"],
            notification_type="follow",
            target_type="user",
            target_id=user_to_follow.id,
            message=f"@{current_user.username} started following you."
        )

        db.session.commit()

        return redirect(request.referrer)


    @app.route("/unfollow/<username>")
    def unfollow_user(username):

        if "user_id" not in session:
            return "Unauthorized", 401

        user_to_unfollow = User.query.filter_by(
            username=username
        ).first()

        if not user_to_unfollow:
            return "User not found"

        follow = Follow.query.filter_by(
            follower_id=session["user_id"],
            following_id=user_to_unfollow.id
        ).first()

        if follow:

            db.session.delete(follow)

            delete_notification(
                user_id=user_to_unfollow.id,
                actor_id=session["user_id"],
                notification_type="follow",
                target_type="user",
                target_id=user_to_unfollow.id
            )

            db.session.commit()

        return redirect(request.referrer)