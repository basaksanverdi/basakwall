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
        db.ForeignKey("users.id"),
        nullable=False
    )

    following_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    follower = db.relationship(
        "User",
        foreign_keys=[follower_id],
        backref="following_relationships"
    )

    following = db.relationship(
        "User",
        foreign_keys=[following_id],
        backref="follower_relationships"
    )