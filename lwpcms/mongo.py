from pymongo import MongoClient
from lwpcms.application import config


client = MongoClient('localhost', 27017)
db = client[config['database']['name']]
