from app import app
from flask import render_template
from . import models


@app.route('/')
def show_db():
    my_cursor = models.db.vacancy_collection.find({})
    return render_template('show_db.html', cursor=my_cursor)
