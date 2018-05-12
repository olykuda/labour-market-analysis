from random import choice
from scraping.constants import CATEGORIES, CITIES
from app import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1


class TestVacancy(db.Model):
    __tablename__ = 'vacancy_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    city = db.Column(db.String(25))
    company = db.Column(db.String(25))
    category = db.Column(db.String(25))
    date_published = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(TestVacancy, self).__init__(**kwargs)

    @staticmethod
    def bootstrap(count):
        from mimesis import Business, Datetime

        for _ in range(count):
            vacancy = TestVacancy(
                id=_,
                title='',
                city=choice(CITIES),
                company=Business('en').company(),
                date_published=datetime.strptime(Datetime('uk').date(start=2013, end=2017, fmt=''), "%d.%m.%Y"),
                category=choice(CATEGORIES)
            )
            db.session.add(vacancy)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
