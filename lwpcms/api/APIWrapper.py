from urllib.parse import urljoin
import requests
import json


class APIWrapper(object):
    """
    This class is used to talk to another LWPCMS site.
    """

    def __init__(self, host):
        self.host = host
        self.query_endpoint = urljoin(host, 'api/query')
        self.headers = {'Content-Type': 'application/json'}


    def query(self, query):
        response = requests.post(
                self.query_endpoint,
                json.dumps(query),
                headers=self.headers
                )
        
        return json.loads(response.text)
