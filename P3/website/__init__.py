from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "mysecretkey"

    from .views import view
    from .auth import auth

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
