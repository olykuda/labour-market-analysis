from app import app
from flask import render_template, url_for, send_file
from . import models
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.pyplot import mpld3
from .analysis.prep_data import PrepData
#from .analysis.arima import ARIMA
from scraping.constants import CATEGORIES, CITIES


@app.route('/', methods=['GET', 'POST'])
def dropdown():
    return render_template('index.html',
                           categories=CATEGORIES,
                           cities=CITIES)


@app.route('/test')
def test():
    prep_data = PrepData()
    # df = prep_data.sort_df_dates(prep_data.create_time_series())
    df = prep_data.create_time_series()
    return render_template("test.html", name='dataframe', data=df.to_html(escape=False))


@app.route('/arima')
def arima_test():
    return render_template('forecast.html',)


@app.route('/db')
def show_db():
    my_cursor = models.db.vacancy_collection.find({})
    return render_template('show_db.html', cursor=my_cursor)


# @app.route('/models')
# def plot(cat='Java'):
#     arima_tst = ARIMA()
#     plt.figure(figsize=(15, 7))
#     df = arima_tst.create_dataframe()
#     df.count.plot(y='count of vacancies')
#     plt.ylabel('Count of vacancies')
#     img = BytesIO()
#     plt.savefig(img)
#     img.seek(0)
#     #pylab.show()
#     return send_file(img, mimetype='image/png')
#     #return render_template('statistics.html', title='Current statistics', cursor=my_cursor, figure=)
#     # df = ARIMA.read_mongo()
#     # return render_template("test.html", name='dataframe', data=df)
