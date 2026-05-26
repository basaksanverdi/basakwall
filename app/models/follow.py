from database import db
from datetime import datetime


class Follow(db.Model):

    __tablename__ = "follows"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    follower_id = db.Column(
        db.Integer,
        nullable=False
    )

    following_id = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )