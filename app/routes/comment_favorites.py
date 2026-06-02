from flask import session, redirect, request, render_template
from database import db

from app.models.comment import Comment
from app.models.comment_favorite import CommentFavorite


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
        db.session.commit()

        return redirect(request.referrer)


    @app.route("/comment_unfav/<int:comment_id>")
    def unfavorite_comment(comment_id):

        if "user_id" not in session:
            return redirect("/login")

        favorite = CommentFavorite.query.filter_by(
            user_id=session["user_id"],
            comment_id=comment_id
        ).first()

        if favorite:

            db.session.delete(favorite)
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