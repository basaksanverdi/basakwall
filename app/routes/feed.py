from flask import render_template, session, redirect
from app.models.post import Post
from app.models.follow import Follow
from app.models.user import User


def register_feed_routes(app):

    @app.route("/feed")
    def feed():

        if "user_id" not in session:
            return redirect("/login")

        following = Follow.query.filter_by(
            follower_id=session["user_id"]
        ).all()

        following_ids = [
            follow.following_id
            for follow in following
        ]

        following_ids.append(
            session["user_id"]
        )

        current_user = User.query.get(
            session["user_id"]
        )

        posts = Post.query.filter(
            Post.user_id.in_(following_ids)
        ).order_by(
            Post.created_at.desc()
        ).all()

        return render_template(
            "feed.html",
            posts=posts,
            current_user=current_user
        )