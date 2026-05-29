from flask import session, redirect, request, render_template
from database import db
from app.models.favorite import Favorite
from app.models.post import Post


def register_favorite_routes(app):

    @app.route("/fav/<int:post_id>")
    def favorite_post(post_id):

        existing_favorite = Favorite.query.filter_by(
            user_id=session["user_id"],
            post_id=post_id
        ).first()

        if existing_favorite:
            return redirect("/feed")

        favorite = Favorite(
            user_id=session["user_id"],
            post_id=post_id
        )

        db.session.add(favorite)
        db.session.commit()

        return redirect(request.referrer)


    @app.route("/unfav/<int:post_id>")
    def unfavorite_post(post_id):

        favorite = Favorite.query.filter_by(
            user_id=session["user_id"],
            post_id=post_id
        ).first()

        if favorite:

            db.session.delete(favorite)
            db.session.commit()

        return redirect(request.referrer)

    @app.route("/post/<int:post_id>/favorites")
    def post_favorites(post_id):

        post = Post.query.get_or_404(post_id)

        favorites = Favorite.query.filter_by(
            post_id=post.id
        ).all()

        return render_template(
            "post_favorites.html",
            post=post,
            favorites=favorites
        )