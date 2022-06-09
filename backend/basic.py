import requests

endpoint = "http://localhost:8000/cluster"

getResponse = requests.get(endpoint,params={"abc",123}, json={"query":"Hello world"})