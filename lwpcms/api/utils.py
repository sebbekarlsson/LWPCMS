import requests
import json


def lwpcms_query_remote(remote_url, query):
    response = requests.post(remote_url + 'api/query', json.dumps(query), headers={'Content-Type': 'application/json'})
    
    return json.loads(response.text)
