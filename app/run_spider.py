# import json
# import requests
#
# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def show_vacancies():
#     params = {
#         'spider_name': 'vacancy_spider',
#         'start_requests': True
#     }
#     response = requests.get('http://localhost:9080/result.json', params)
#     data = json.loads(response.text)
#     result = '\n'.join(item['title'] +'  '+ item['city']+'  '+ item['company']+'  '+ item['date_published']+'  '+ item['category']
#                        for item in data['items'])
#     return result
