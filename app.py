from flask import Flask, render_template
from config import Config
from database import db

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.config.from_object(Config)

db.init_app(app)

from app.routes.auth import register_routes
from app.routes.profile import register_profile_routes
from app.routes.follows import register_follow_routes
from app.routes.posts import register_post_routes
from app.routes.feed import register_feed_routes
from app.routes.discover import register_discover_routes

register_routes(app)
register_profile_routes(app)
register_follow_routes(app)
register_post_routes(app)
register_feed_routes(app)
register_discover_routes(app)

with app.app_context():

    from app.models.user import User
    from app.models.follow import Follow
    from app.models.post import Post

    db.create_all()


@app.route("/")
def home():

    return render_template("index.html")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    