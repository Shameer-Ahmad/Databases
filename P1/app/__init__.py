import os
from flask import Flask, session
from flask_login import LoginManager
from app.db import init_db
import secrets



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
         DATABASE=os.path.join(app.instance_path, 'northwind-SQLite3', 'dist', 'northwind.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

     # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.db import get_db
        user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        return user

    # Initialize the database
    from . import db
    db.init_app(app)

    with app.app_context():
        init_db()
    
    from . import auth, landing, cart, categories, search 
    app.register_blueprint(auth.bp)
    app.register_blueprint(landing.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(search.bp)

    @app.before_request
    def create_session():
        if "shopper_id" not in session:
            session["shopper_id"] = secrets.token_hex(16)  # Generates a unique random shopper ID
    
    return app 
