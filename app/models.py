from random import choice
from scraping.constants import CATEGORIES, CITIES
from app import client
import pymongo
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

db = client.labour_market_db


class TestVacancy():
    def __init__(self, **kwargs):
        super(TestVacancy, self).__init__(**kwargs)

    @staticmethod
    def bootstrap(count):
        from mimesis import Business, Datetime

        for _ in range(count):
            #_id = _
            title = str(_)
            city = choice(CITIES)
            category = choice(CATEGORIES)
            company = Business('en').company()
            date_published = datetime.strptime(Datetime('uk').date(start=2013, end=2017, fmt=''), "%d.%m.%Y")
            vacancy = {
                          #"_id": _id,
                          "title": title,
                          "city": city,
                          "company": company,
                          "category": category,
                          "date_published": date_published
            }
            db.vacancy_collection.insert(vacancy)
