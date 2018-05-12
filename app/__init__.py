from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from . import views
from . import models


db.app = app
db.init_app(app)
db.create_all()
models.TestVacancy().bootstrap(count=1000)
