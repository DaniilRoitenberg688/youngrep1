from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.execel_connector import ExcelConnector
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'admin.login'


data_base = ExcelConnector()
end_age = 18

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)


from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')


from app import models
