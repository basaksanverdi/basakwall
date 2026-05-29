from flask import render_template, session, redirect
from sqlalchemy import desc

from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post


def register_discover_routes(app):

    @app.route("/discover")
    def discover():

        if "user_id" not in session:
            return redirect("/login")

        current_user_id = session["user_id"]

        followed_users = Follow.query.filter_by(
            follower_id=current_user_id
        ).all()

        followed_user_ids = [
            follow.following_id for follow in followed_users
        ]

        followed_user_ids.append(current_user_id)

        discover_users = User.query.filter(
            ~User.id.in_(followed_user_ids)
        ).all()

        discover_posts = Post.query.filter(
            ~Post.user_id.in_(followed_user_ids)
        ).order_by(desc(Post.created_at)).all()

        return render_template(
            "discover.html",
            discover_users=discover_users,
            discover_posts=discover_posts
        )