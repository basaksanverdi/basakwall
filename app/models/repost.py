from database import db
from datetime import datetime, timezone


class Repost(db.Model):

    __tablename__ = "reposts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=True
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        backref="reposts"
    )

    post = db.relationship(
        "Post",
        backref="reposts"
    )

    comment = db.relationship(
        "Comment",
        backref="reposts"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_user_post_repost"
        ),
        db.UniqueConstraint(
            "user_id",
            "comment_id",
            name="unique_user_comment_repost"
        ),
        db.CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR "
            "(post_id IS NULL AND comment_id IS NOT NULL)",
            name="only_one_repost_target"
        ),
    )