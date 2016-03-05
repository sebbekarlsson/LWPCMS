import requests
import json


def lwpcms_query_remote(remote_url, query):
    response = requests.post(remote_url + 'api/query', json.dumps(query), headers={'Content-Type': 'application/json'})
    print(response.text)


#lwpcms_query_remote('http://demo.lwpcms.com/', {
#        'query': {
#            'structure': '#User'
#            }
#    })
