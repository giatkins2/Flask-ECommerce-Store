from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# init my Login Manager
login = LoginManager()
# Do inits for database stuff
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    #init the app
    app = Flask(__name__)

    #link our config to oour app
    app.config.from_object(config_class)

    # register plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # This is where you will be sent if you are not logged
    # into trying to go to a login required page
    login.login_view='auth.login'
    login.login_message = 'Please login before you continue.'
    login.login_message_category='is-warning'

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.shop import bp as shop_bp
    app.register_blueprint(shop_bp)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app