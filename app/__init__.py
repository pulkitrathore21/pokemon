from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

from . import views

app.register_blueprint(views.pokemonapi)

app.config.from_pyfile("config.py")
db.init_app(app)
from .models import Pokemon

app.app_context().push()
db.create_all()
