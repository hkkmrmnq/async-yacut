from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .converters import RegexConverter
from .settings import Config


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.url_map.converters['re'] = RegexConverter

from . import api_views, error_handlers, models, views
