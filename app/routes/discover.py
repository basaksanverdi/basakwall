from flask import render_template, session, redirect
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post
from app.models.favorite import Favorite
from app.models.comment_favorite import CommentFavorite
from app.models.comment import Comment
from app.models.repost import Repost

from datetime import datetime


def normalize_sort_date(created_at):

    if created_at is None:
        return datetime.min

    return created_at.replace(tzinfo=None)


def register_discover_routes(app):

    @app.route("/discover")
    def discover():

        if "user_id" not in session:
            return redirect("/login")

        current_user_id = session["user_id"]

        current_user = User.query.get(
            current_user_id
        )

        followed_users = Follow.query.filter_by(
            follower_id=current_user_id
        ).all()

        followed_user_ids = [
            follow.following_id
            for follow in followed_users
        ]

        followed_user_ids.append(
            current_user_id
        )

        discover_users = User.query.filter(
            ~User.id.in_(followed_user_ids)
        ).all()

        discover_posts = Post.query.filter(
            ~Post.user_id.in_(followed_user_ids)
        ).order_by(
            desc(Post.created_at)
        ).all()

        discover_reposts = Repost.query.options(
            joinedload(Repost.user),
            joinedload(Repost.post),
            joinedload(Repost.comment).joinedload(Comment.post)
        ).filter(
            ~Repost.user_id.in_(followed_user_ids)
        ).order_by(
            desc(Repost.created_at)
        ).all()

        discover_items = []

        for post in discover_posts:

            discover_items.append({
                "type": "post",
                "created_at": post.created_at,
                "post": post,
                "comment": None,
                "repost": None
            })

        for repost in discover_reposts:

            if repost.post_id is not None and repost.post:

                discover_items.append({
                    "type": "repost_post",
                    "created_at": repost.created_at,
                    "post": repost.post,
                    "comment": None,
                    "repost": repost
                })

            elif repost.comment_id is not None and repost.comment:

                discover_items.append({
                    "type": "repost_comment",
                    "created_at": repost.created_at,
                    "post": repost.comment.post,
                    "comment": repost.comment,
                    "repost": repost
                })

        discover_items = sorted(
            discover_items,
            key=lambda item: normalize_sort_date(item["created_at"]),
            reverse=True
        )

        favorited_post_ids = [

            favorite.post_id

            for favorite in Favorite.query.filter_by(
                user_id=current_user_id
            ).all()

        ]

        favorited_comment_ids = [

            favorite.comment_id

            for favorite in CommentFavorite.query.filter_by(
                user_id=current_user_id
            ).all()

        ]

        reposted_post_ids = [

            repost.post_id

            for repost in Repost.query.filter_by(
                user_id=current_user_id
            ).filter(
                Repost.post_id.isnot(None)
            ).all()

        ]

        reposted_comment_ids = [

            repost.comment_id

            for repost in Repost.query.filter_by(
                user_id=current_user_id
            ).filter(
                Repost.comment_id.isnot(None)
            ).all()

        ]

        return render_template(
            "discover.html",
            current_user=current_user,
            discover_users=discover_users,
            discover_posts=discover_posts,
            discover_items=discover_items,
            favorited_post_ids=favorited_post_ids,
            favorited_comment_ids=favorited_comment_ids,
            reposted_post_ids=reposted_post_ids,
            reposted_comment_ids=reposted_comment_ids
        )