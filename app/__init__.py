from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config, config
from aiogram import Bot

db = SQLAlchemy()
migrate = Migrate(render_as_batch=True)
login = LoginManager()
login.login_view = "admin.login"



data_base = None
end_age = 18


def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")


    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
