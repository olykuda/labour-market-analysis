from scrapy import Item, Field
from scrapy.loader.processors import MapCompose
from scraping.constants import MONTHS
import re


def date_prep(date_str):
    #date_str == '11 октября 2014'
    for key, value in MONTHS:
        re.sub(key, value, date_str)
    result = re.sub(' ', '/', date_str)
    return result


def salary_prep(salary_str):
    """"
    return: a salary string in format '$d-d'
    """
    re.sub('до ', '0-', salary_str)
    if re.match('от ', salary_str):
        re.sub('до ', '', salary_str)
        salary_str += '+'
    return salary_str


def city_prep(lst):
    for i in range(len(lst)):
        if lst[i] == 'удаленно':
            lst.pop(i)
    return lst


class ScrapingItem(Item):
    # _id = Field()
    title = Field()
    city = Field(input_processor=MapCompose(city_prep))
    company = Field()
    date_published = Field(input_processor=MapCompose(date_prep))
    #salary = Field(input_processor=MapCompose(salary_prep))
    # salary = Field(input_processor=MapCompose(parse_salary))
    category = Field()
    # is_open = Field()
    # url = Field()
