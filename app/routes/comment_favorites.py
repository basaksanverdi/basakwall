from flask import session, redirect, request, render_template
from database import db

from app.models.comment import Comment
from app.models.comment_favorite import CommentFavorite
from app.models.user import User
from app.routes.notifications import create_notification, delete_notification


def register_comment_favorite_routes(app):

    @app.route("/comment_fav/<int:comment_id>")
    def favorite_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return redirect(request.referrer)

        existing_favorite = CommentFavorite.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if existing_favorite:
            return redirect(request.referrer)

        favorite = CommentFavorite(
            user_id=session["user_id"],
            comment_id=comment_id
        )

        db.session.add(favorite)

        current_user = User.query.get(session["user_id"])

        create_notification(
            user_id=comment.user_id,
            actor_id=session["user_id"],
            notification_type="comment_favorite",
            target_type="comment",
            target_id=comment.id,
            message=f"@{current_user.username} favorited your comment."
        )

        db.session.commit()

        return redirect(request.referrer)


    @app.route("/comment_unfav/<int:comment_id>")
    def unfavorite_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return redirect(request.referrer)

        favorite = CommentFavorite.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if favorite:

            db.session.delete(favorite)

            delete_notification(
                user_id=comment.user_id,
                actor_id=session["user_id"],
                notification_type="comment_favorite",
                target_type="comment",
                target_id=comment.id
            )

            db.session.commit()

        return redirect(request.referrer)


    @app.route("/comment/<int:comment_id>/favorites")
    def comment_favorites(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        comment = Comment.query.get(comment_id)

        if not comment:
            return "Comment not found", 404

        favorites = CommentFavorite.query.filter_by(
            comment_id=comment.id
        ).all()

        return render_template(
            "comment_favorites.html",
            comment=comment,
            favorites=favorites
        )