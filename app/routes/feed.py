from flask import render_template, session, redirect
from app.models.post import Post
from app.models.follow import Follow
from app.models.user import User
from app.models.favorite import Favorite
from app.models.comment_favorite import CommentFavorite
from app.models.comment import Comment
from app.models.repost import Repost
from sqlalchemy.orm import joinedload

from datetime import datetime


def normalize_sort_date(created_at):

    if created_at is None:
        return datetime.min

    return created_at.replace(tzinfo=None)


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

        reposts = Repost.query.options(
            joinedload(Repost.post),
            joinedload(Repost.comment).joinedload(Comment.post)
        ).filter(
            Repost.user_id.in_(following_ids)
        ).order_by(
            Repost.created_at.desc()
        ).all()

        feed_items = []

        for post in posts:

            feed_items.append({
                "type": "post",
                "created_at": post.created_at,
                "post": post,
                "comment": None,
                "repost": None
            })

        for repost in reposts:

            if repost.post_id is not None and repost.post:

                feed_items.append({
                    "type": "repost_post",
                    "created_at": repost.created_at,
                    "post": repost.post,
                    "comment": None,
                    "repost": repost
                })

            elif repost.comment_id is not None and repost.comment:

                feed_items.append({
                    "type": "repost_comment",
                    "created_at": repost.created_at,
                    "post": repost.comment.post,
                    "comment": repost.comment,
                    "repost": repost
                })

        feed_items = sorted(
            feed_items,
            key=lambda item: normalize_sort_date(item["created_at"]),
            reverse=True
        )

        favorited_post_ids = [

            favorite.post_id

            for favorite in Favorite.query.filter_by(
                user_id=session["user_id"]
            ).all()

        ]

        favorited_comment_ids = [

            favorite.comment_id

            for favorite in CommentFavorite.query.filter_by(
                user_id=session["user_id"]
            ).all()

        ]

        reposted_post_ids = [

            repost.post_id

            for repost in Repost.query.filter_by(
                user_id=session["user_id"]
            ).filter(
                Repost.post_id.isnot(None)
            ).all()

        ]

        reposted_comment_ids = [

            repost.comment_id

            for repost in Repost.query.filter_by(
                user_id=session["user_id"]
            ).filter(
                Repost.comment_id.isnot(None)
            ).all()

        ]

        return render_template(
            "feed.html",
            posts=posts,
            feed_items=feed_items,
            current_user=current_user,
            favorited_post_ids=favorited_post_ids,
            favorited_comment_ids=favorited_comment_ids,
            reposted_post_ids=reposted_post_ids,
            reposted_comment_ids=reposted_comment_ids
        )