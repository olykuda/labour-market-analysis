from scraping.scraping.items import ScrapingItem
from scraping.constants import CATEGORIES
from urllib.parse import quote_plus, unquote_plus
import scrapy
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class ScrapingSpider(scrapy.Spider):
    name = 'vacancy_spider'
    domain = "http://jobs.dou.ua"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["http://jobs.dou.ua/vacancies/?category=.NET"]
    # start_urls = ["http://jobs.dou.ua/vacancies/?category=Unity"]
    cat_iter = iter(CATEGORIES)

    def __init__(self):
        self.driver = webdriver.Firefox()

    @staticmethod
    def __get_title(response):
        title = response.css('.b-vacancy > h1[class=g-h2]::text').extract_first()
        return title

    @staticmethod
    def __get_city(response):
        city = response.css('.sh-info > span[class=place]::text').extract()
        return city

    @staticmethod
    def __get_salary(response):
        salary = response.css('.sh-info > span[class=salary]::text').extract_first()
        return salary

    @staticmethod
    def __get_company(response):
        city = response.css('.info > div[class=l-n] > a::text').extract_first()
        return city

    @staticmethod
    def __get_date_published(response):
        date = response.css('.b-vacancy > div[class=date]::text').extract_first()
        return date

    def parse(self, response):
        self.driver.get(response.url)
        # more_vacancies = self.driver.find_element_by_xpath('//p[@class="footer-lang-switch"]/a[@href=""]')
        # more_vacancies.click()
        # time.sleep(5)
        while True:
            try:
                more_vacancies = self.driver.find_element_by_xpath('//div[@class="more-btn"]/a')
                more_vacancies.click()
                time.sleep(3)
            except ElementNotInteractableException:
                break
            except NoSuchElementException:
                break

        vacancies = self.driver.find_elements_by_class_name('vt')
        vacancies_urls = []
        for vacancy in vacancies:
            vacancies_urls.append(vacancy.get_attribute('href'))

        # for url in vacancies_urls:
        #     category = unquote_plus(re.split(r'=', response.url)[1])
        #     print(category)
        #     print(url)

        for url in vacancies_urls:
            category = unquote_plus(re.split(r'=', response.url)[1])
            yield scrapy.Request(url=url,
                                 callback=self.parse_vacancy,
                                 meta={'Category': category})
        try:
            next_category = next(self.cat_iter)
            next_url = 'http://jobs.dou.ua/vacancies/?category=' + quote_plus(next_category)
            yield scrapy.Request(url=next_url,
                                 callback=self.parse)
        except StopIteration:
            self.driver.close()

    def parse_vacancy(self, response):
        item = ScrapingItem()

        # item['_id'] =
        item['title'] = self.__get_title(response)
        item['city'] = self.__get_city(response)
        item['company'] = self.__get_company(response)
        item['date_published'] = self.__get_date_published(response)
        #item['salary'] = self.__get_salary(response)
        item['category'] = response.meta.get('Category')
        # item['url'] = self.__get_url(response)

        yield item
