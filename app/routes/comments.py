from flask import request, session, redirect
from app.models.comment import Comment
from app.models.post import Post
from database import db


def register_comment_routes(app):

    @app.route("/comment/<int:post_id>", methods=["POST"])
    def create_comment(post_id):

        if "user_id" not in session:
            return "Unauthorized", 401

        post = Post.query.get(post_id)

        if not post:
            return "Post not found", 404

        content = request.form.get("content")

        if not content:
            return redirect(f"/posts/{post_id}")

        comment = Comment(
            content=content,
            user_id=session["user_id"],
            post_id=post_id
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(f"/posts/{post_id}")