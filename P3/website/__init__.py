from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "mysecretkey"
    app.config['VERIFICATION_CODE'] = "foodies"

    from .views import views
    from .auth import auth
    from .restaurants import restaurants
    from .reviews import reviews
    from .events import events

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(restaurants, url_prefix="/restaurants")
    app.register_blueprint(reviews, url_prefix="/reviews")
    app.register_blueprint(events, url_prefix="/events")

    return app
