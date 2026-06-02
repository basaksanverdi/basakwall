from flask import request, session, redirect, render_template
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
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


    @app.route("/comments/<int:comment_id>")
    def view_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        current_user = User.query.get(session["user_id"])

        post = comment.post

        other_comments = [
            c for c in post.comments
            if c.id != comment.id
        ]

        favorited_comment_ids = [
            favorite.comment_id
            for favorite in current_user.comment_favorites
        ]

        return render_template(
            "comment.html",
            comment=comment,
            post=post,
            other_comments=other_comments,
            current_user=current_user,
            favorited_comment_ids=favorited_comment_ids
        )