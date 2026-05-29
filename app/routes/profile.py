from flask import render_template, session
from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post
from sqlalchemy.orm import joinedload

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def register_profile_routes(app):

    @app.route("/profile/<username>")
    def user_profile(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        follower_count = Follow.query.filter_by(
            following_id=user.id
        ).count()

        following_count = Follow.query.filter_by(
            follower_id=user.id
        ).count()

        is_following = Follow.query.filter_by(
            follower_id=session["user_id"],
            following_id=user.id
        ).first() is not None

        posts = Post.query.filter_by(
            user_id=user.id
        ).order_by(
            Post.created_at.desc()
        ).all()

        is_owner = (
            session["user_id"] == user.id
        )

        is_online = False

        if user.last_activity:

            now = datetime.now(
                ZoneInfo("Europe/Istanbul")
            )

            last_activity = user.last_activity.replace(
                tzinfo=ZoneInfo("Europe/Istanbul")
            )

            difference = now - last_activity

            if difference < timedelta(minutes=1):

                is_online = True

        print(session)

        return render_template(
            "profile.html",
            user=user,
            current_user=session["username"],
            follower_count=follower_count,
            following_count=following_count,
            is_following=is_following,
            posts=posts,
            is_owner=is_owner,
            is_online=is_online
        )

    @app.route("/profile/<username>/followers")
    def followers(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        followers = Follow.query.options(
            joinedload(Follow.follower)
        ).filter_by(
            following_id=user.id
        ).all()

        return render_template(
            "followers.html",
            user=user,
            followers=followers
        )

    @app.route("/profile/<username>/following")
    def following(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        following = Follow.query.options(
            joinedload(Follow.following)
        ).filter_by(
            follower_id=user.id
        ).all()

        return render_template(
            "following.html",
            user=user,
            following=following
        )