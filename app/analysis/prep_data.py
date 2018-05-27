import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#import statsmodels.api as sm
from app import models
#from .forecast import ForecastModel
import pandas as pd
import datetime


class PrepData:
    @staticmethod
    def count_items(category, city, date_published):
        return models.db.vacancy_collection.count({'category': category,
                                                   'city': city,
                                                   'date_published': date_published})

    @staticmethod
    def read_mongo(category, city):
        _db = models.db.vacancy_collection.find({'category': category, 'city': city})
        _fields = ['city', 'category', 'date_published']
        df = pd.DataFrame(data=list(_db), columns=_fields)
        return df

    # def create_dataframe(self, category='Java', city='Киев'):
    #     _df = self.read_mongo(category, city)
    #     dates = []
    #     counts = []
    #     for index, row in _df.iterrows():
    #         dates.append(row['date_published'])
    #
    #     date_ind = []
    #     for i in range(len(dates)):
    #         counts.append(self.count_items(category, city, dates[i]))
    #         date_ind.append(i)
    #     result_dict = {
    #         'date_published': dates,
    #         'count': counts
    #     }
    #     df = pd.DataFrame(result_dict, index=date_ind)
    #     return df

    @staticmethod
    def parse_date(date):
        # date_str = date.split('-')
        # date_dict = {'year': date_str[0], 'month': date_str[1], 'day': date_str[2]}
        dict_date = date.time_tuple()
        date_dict = {'year': dict_date[0], 'month': dict_date[1], 'day': dict_date[2]}
        return date_dict

    def sort_df_dates(self, _df):
        df = pd.DataFrame()
        timestamps = _df['date_published'].tolist()
        dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in timestamps]
        dates.sort()
        sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
        for i in range(0, len(sorteddates)):
            for index, row in _df.iterrows():
                if sorteddates[i] == row['date_published']:
                    df.append(row)
                    break
        return df

    @staticmethod
    def get_time_interval(dates):
        dict_date = dates[0].time_tuple()
        first_year = dict_date[0]
        first_month = dict_date[1]
        first_day = dict_date[2]
        if first_day < 10:
            first_day = 10
        elif first_day < 20:
            first_day = 20
        else:
            first_day = 1
        last_year = dict_date[0]
        last_month = dict_date[1]
        last_day = dict_date[2]
        if last_day < 10:
            last_day = 10
        elif last_day < 20:
            last_day = 20
        else:
            last_day = 1
        return ({'first_year': first_year, 'first_month': first_month, 'first_day': first_day},
                {'last_year': last_year, 'last_month': last_month, 'last_day': last_day})

    def get_series_dates(self, _df, dates):
        df = self.sort_df_dates(_df)
        time_interval = self.get_time_interval(dates)
        list_interval_dates = []
        series_dates = {}
        first_year = time_interval[0]['first_year']
        last_year = time_interval[1]['last_year']
        first_month = time_interval[0]['first_month']
        last_month = time_interval[1]['last_month']
        first_day = time_interval[0]['first_day']
        last_day = time_interval[1]['last_day']
        month = first_month
        day = first_day
        # записываем к каждой дате временного ряда список дат существования вакансии
        for year in range(first_year, last_year):
            while month <= 12:
                while day <= 31:
                    date_dict = self.parse_date(df['date_published'])
                    day_pub = date_dict['day']
                    month_pub = date_dict['month']
                    year_pub = date_dict['year']
                    if day_pub == day and month_pub == month and year_pub == year:
                        list_interval_dates.append(df['date_published'])
                    if day == 1 or day == 10 or day == 20:
                        series_dates[datetime.date(year, month, day)] = list_interval_dates
                        list_interval_dates = []
                    if year == last_year and month == last_month and day == last_day:
                        break
                    day += 1
                month += 1
                day = 1
            month = 1

        return series_dates

    def create_dataframe(self, dates, category, city):
        counts = []
        date_ind = []
        for i in range(len(dates)):
            counts.append(self.count_items(category, city, dates[i]))
            date_ind.append(i)
        result_dict = {
            'date_published': dates,
            'count': counts
        }
        df = pd.DataFrame(result_dict, index=date_ind)
        return df

    def create_time_series(self, category='Java', city='Киев'):
        _df = self.read_mongo(category, city)
        dates = _df['date_published'].tolist()

        # dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in timestamps]
        # series_dates = self.get_series_dates(_df, dates)
        # df = self.create_dataframe(series_dates, category, city)
        df = self.create_dataframe(dates, category, city)
        return df
