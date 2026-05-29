from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    profile_picture = db.Column(
        db.String(255),
        default="default.png"
    )

    posts = db.relationship(
        "Post",
        backref="author",
        lazy=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("Europe/Istanbul")
        )
    )

    last_seen = db.Column(
        db.DateTime,
        nullable=True,
        default=None
    )

    is_online = db.Column(
        db.Boolean,
        default=False
    )