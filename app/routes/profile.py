from flask import render_template, session
from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post
from app.models.favorite import Favorite
from app.models.comment import Comment
from app.models.comment_favorite import CommentFavorite
from app.models.repost import Repost
from sqlalchemy.orm import joinedload

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def normalize_sort_date(created_at):

    if created_at is None:
        return datetime.min

    return created_at.replace(tzinfo=None)


def register_profile_routes(app):

    @app.route("/profile/<username>")
    def user_profile(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        follower_count = Follow.query.filter_by(
            following_id=user.id
        ).count()

        following_count = Follow.query.filter_by(
            follower_id=user.id
        ).count()

        is_following = Follow.query.filter_by(
            follower_id=session["user_id"],
            following_id=user.id
        ).first() is not None

        posts = Post.query.filter_by(
            user_id=user.id
        ).order_by(
            Post.created_at.desc()
        ).all()

        reposts = Repost.query.options(
            joinedload(Repost.post),
            joinedload(Repost.comment).joinedload(Comment.post)
        ).filter_by(
            user_id=user.id
        ).order_by(
            Repost.created_at.desc()
        ).all()

        profile_items = []

        for post in posts:

            profile_items.append({
                "type": "post",
                "created_at": post.created_at,
                "post": post,
                "comment": None,
                "repost": None
            })

        for repost in reposts:

            if repost.post_id is not None and repost.post:

                profile_items.append({
                    "type": "repost_post",
                    "created_at": repost.created_at,
                    "post": repost.post,
                    "comment": None,
                    "repost": repost
                })

            elif repost.comment_id is not None and repost.comment:

                profile_items.append({
                    "type": "repost_comment",
                    "created_at": repost.created_at,
                    "post": repost.comment.post,
                    "comment": repost.comment,
                    "repost": repost
                })

        profile_items = sorted(
            profile_items,
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

        is_owner = (
            session["user_id"] == user.id
        )

        is_online = False

        if user.last_activity:

            now = datetime.now(
                ZoneInfo("Europe/Istanbul")
            )

            last_activity = user.last_activity.replace(
                tzinfo=ZoneInfo("Europe/Istanbul")
            )

            difference = now - last_activity

            if difference < timedelta(minutes=1):

                is_online = True

        print(session)

        return render_template(
            "profile.html",
            user=user,
            current_user=session["username"],
            follower_count=follower_count,
            following_count=following_count,
            is_following=is_following,
            posts=posts,
            profile_items=profile_items,
            is_owner=is_owner,
            is_online=is_online,
            favorited_post_ids=favorited_post_ids,
            favorited_comment_ids=favorited_comment_ids,
            reposted_post_ids=reposted_post_ids,
            reposted_comment_ids=reposted_comment_ids
        )

    @app.route("/profile/<username>/comments")
    def profile_comments(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        comments = Comment.query.options(
            joinedload(Comment.post)
        ).filter_by(
            user_id=user.id
        ).order_by(
            Comment.created_at.desc()
        ).all()

        return render_template(
            "profile_comments.html",
            user=user,
            comments=comments
        )

    @app.route("/profile/<username>/followers")
    def followers(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        followers = Follow.query.options(
            joinedload(Follow.follower)
        ).filter_by(
            following_id=user.id
        ).all()

        return render_template(
            "followers.html",
            user=user,
            followers=followers
        )

    @app.route("/profile/<username>/following")
    def following(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        following = Follow.query.options(
            joinedload(Follow.following)
        ).filter_by(
            follower_id=user.id
        ).all()

        return render_template(
            "following.html",
            user=user,
            following=following
        )

    @app.route("/profile/<username>/favorites")
    def user_favorites(username):

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "User not found"

        post_favorites = Favorite.query.filter_by(
            user_id=user.id
        ).all()

        comment_favorites = CommentFavorite.query.filter_by(
            user_id=user.id
        ).all()

        unified_favorites = []

        for favorite in post_favorites:

            unified_favorites.append({
                "type": "post",
                "created_at": favorite.created_at,
                "favorite": favorite
            })

        for favorite in comment_favorites:

            unified_favorites.append({
                "type": "comment",
                "created_at": favorite.created_at,
                "favorite": favorite
            })

        unified_favorites = sorted(
            unified_favorites,
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

        return render_template(
            "profile_favorites.html",
            user=user,
            unified_favorites=unified_favorites,
            favorited_post_ids=favorited_post_ids,
            favorited_comment_ids=favorited_comment_ids
        )