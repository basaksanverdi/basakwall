from flask import request, redirect, session, render_template
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
from app.models.repost import Repost
from app.models.notification import Notification
from database import db


def register_post_routes(app):

    @app.route("/posts", methods=["POST"])
    def create_post():

        if "user_id" not in session:
            return redirect("/login")

        content = request.form.get("content")

        if not content:
            return redirect(request.referrer)

        new_post = Post(
            content=content,
            user_id=session["user_id"]
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(request.referrer)


    @app.route("/delete_post/<int:post_id>")
    def delete_post(post_id):

        if "user_id" not in session:
            return redirect("/login")

        post = Post.query.get(post_id)

        if not post:
            return redirect(request.referrer)

        if post.user_id != session["user_id"]:
            return redirect(request.referrer)

        comments = Comment.query.filter_by(
            post_id=post.id
        ).all()

        for comment in comments:

            comment_notifications = Notification.query.filter_by(
                target_type="comment",
                target_id=comment.id
            ).all()

            for notification in comment_notifications:
                db.session.delete(notification)

        post_notifications = Notification.query.filter_by(
            target_type="post",
            target_id=post.id
        ).all()

        for notification in post_notifications:
            db.session.delete(notification)

        db.session.delete(post)
        db.session.commit()

        return redirect(request.referrer)


    @app.route("/posts/<int:post_id>")
    def view_post(post_id):

        if "user_id" not in session:
            return redirect("/login")

        post = Post.query.get(post_id)

        if not post:
            return "Post not found"

        current_user = User.query.get(session["user_id"])

        favorited_comment_ids = [
            favorite.comment_id
            for favorite in current_user.comment_favorites
        ]

        favorited_post_ids = [
            favorite.post_id
            for favorite in current_user.favorites
        ]

        reposted_post_ids = [
            repost.post_id
            for repost in current_user.reposts
            if repost.post_id is not None
        ]

        reposted_comment_ids = [
            repost.comment_id
            for repost in current_user.reposts
            if repost.comment_id is not None
        ]

        next_page = request.args.get("next")

        return render_template(
            "post.html",
            post=post,
            current_user=current_user,
            next_page=next_page,
            favorited_comment_ids=favorited_comment_ids,
            favorited_post_ids=favorited_post_ids,
            reposted_post_ids=reposted_post_ids,
            reposted_comment_ids=reposted_comment_ids
        )