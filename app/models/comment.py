from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Europe/Istanbul")
        )
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    favorites = db.relationship(
    "CommentFavorite",
    backref="comment",
    lazy=True,
    cascade="all, delete-orphan"
    )   