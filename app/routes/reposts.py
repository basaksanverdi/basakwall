from flask import session, redirect, request, render_template
from database import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.repost import Repost
from app.models.user import User
from app.routes.notifications import create_notification, delete_notification


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

        current_user = User.query.get(session["user_id"])

        create_notification(
            user_id=post.user_id,
            actor_id=session["user_id"],
            notification_type="post_repost",
            target_type="post",
            target_id=post.id,
            message=f"@{current_user.username} reposted your post."
        )

        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/posts/<int:post_id>/unrepost")
    def unrepost_post(post_id):

        if "user_id" not in session:
            return redirect("/login")

        post = Post.query.get(post_id)

        if not post:
            return "Post not found", 404

        repost = Repost.query.filter_by(
            user_id=session["user_id"],
            post_id=post_id
        ).first()

        if not repost:
            return redirect(request.referrer or "/feed")

        db.session.delete(repost)

        delete_notification(
            user_id=post.user_id,
            actor_id=session["user_id"],
            notification_type="post_repost",
            target_type="post",
            target_id=post.id
        )

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

        current_user = User.query.get(session["user_id"])

        create_notification(
            user_id=comment.user_id,
            actor_id=session["user_id"],
            notification_type="comment_repost",
            target_type="comment",
            target_id=comment.id,
            message=f"@{current_user.username} reposted your comment."
        )

        db.session.commit()

        return redirect(request.referrer or "/feed")


    @app.route("/comments/<int:comment_id>/unrepost")
    def unrepost_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        repost = Repost.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if not repost:
            return redirect(request.referrer or "/feed")

        db.session.delete(repost)

        delete_notification(
            user_id=comment.user_id,
            actor_id=session["user_id"],
            notification_type="comment_repost",
            target_type="comment",
            target_id=comment.id
        )

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