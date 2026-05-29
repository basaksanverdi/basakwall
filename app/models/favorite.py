from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Favorite(db.Model):

    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
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

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Europe/Istanbul")
        )
    )

    user = db.relationship(
        "User",
        backref="favorites"
    )

    post = db.relationship(
        "Post",
        backref="favorites"
    )