from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class CommentFavorite(db.Model):

    __tablename__ = "comment_favorites"

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "comment_id"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Europe/Istanbul")
        )
    )