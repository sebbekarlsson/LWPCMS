from pymongo import MongoClient
from lwpcms.config import config


client = MongoClient('localhost', 27017)
db = client[config['database_name']]
