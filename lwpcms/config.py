import json
import os


config_name = 'config.json'
with open(config_name, 'r') as file:
    config = json.loads(file.read())
    file.close()
