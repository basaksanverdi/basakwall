from flask import session, redirect, request, render_template
from database import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.repost import Repost


def register_repost_routes(app):

    @app.route("/posts/<int:post_id>/repost")
    def repost_post(post_id):

        if "user_id" not in session:
            return redirect("/login")

        post = Post.query.get(post_id)

        if not post:
            return "Post not found", 404

        existing_repost = Repost.query.filter_by(
            user_id=session["user_id"],
            post_id=post_id
        ).first()

        if existing_repost:
            return redirect(request.referrer or "/feed")

        repost = Repost(
            user_id=session["user_id"],
            post_id=post_id
        )

        db.session.add(repost)
        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/posts/<int:post_id>/unrepost")
    def unrepost_post(post_id):

        if "user_id" not in session:
            return redirect("/login")

        repost = Repost.query.filter_by(
            user_id=session["user_id"],
            post_id=post_id
        ).first()

        if not repost:
            return redirect(request.referrer or "/feed")

        db.session.delete(repost)
        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/comments/<int:comment_id>/repost")
    def repost_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        existing_repost = Repost.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if existing_repost:
            return redirect(request.referrer or "/feed")

        repost = Repost(
            user_id=session["user_id"],
            comment_id=comment_id
        )

        db.session.add(repost)
        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/comments/<int:comment_id>/unrepost")
    def unrepost_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        repost = Repost.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if not repost:
            return redirect(request.referrer or "/feed")

        db.session.delete(repost)
        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/posts/<int:post_id>/reposts")
    def post_reposts(post_id):

        post = Post.query.get(post_id)

        if not post:
            return "Post not found", 404

        reposts = Repost.query.filter_by(
            post_id=post_id
        ).order_by(
            Repost.created_at.desc()
        ).all()

        return render_template(
            "repost_users.html",
            target_type="post",
            post=post,
            comment=None,
            reposts=reposts
        )


    @app.route("/comments/<int:comment_id>/reposts")
    def comment_reposts(comment_id):

        comment = Comment.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        reposts = Repost.query.filter_by(
            comment_id=comment_id
        ).order_by(
            Repost.created_at.desc()
        ).all()

        return render_template(
            "repost_users.html",
            target_type="comment",
            post=None,
            comment=comment,
            reposts=reposts
        )