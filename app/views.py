from app import app
from flask import render_template
from . import models


@app.route('/')
def show_db():
    return render_template('index.html',
                           rows=models.TestVacancy.query.all()
                           )
