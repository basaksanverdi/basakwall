from database import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Post(db.Model):

    __tablename__ = "posts"

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