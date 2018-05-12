from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
client = MongoClient()
#db = PyMongo(app)
# db = client.labour_market_db

from . import views
from . import models


# db.app = app
# db.init_app(app)
# db.create_all()
models.TestVacancy().bootstrap(count=100)
