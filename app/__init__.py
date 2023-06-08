from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow(app)
migrate = Migrate(app, db)

try:
    from app import views

    app.register_blueprint(views.pokemonapi)
except Exception as e:
    print(f"Error: {e}")

app.config.from_pyfile("config.py")
db.init_app(app)

from .models import Pokemon

app.app_context().push()
