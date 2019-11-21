# Insert to Cassandra and Elasticsearch
import json
from elasticsearch import Elasticsearch
import make_subtitles
import random
import requests

texts = make_subtitles.get_all_texts()

host = "http://localhost:8080/"
rooms = [1, 2, 3, 4, 5, 6]
users = ['lisa', 'kenny', 'voldy']
count = 0
for text in texts:
    room = random.choice(rooms)
    user = random.choice(users)
    url = f"{host}/{room}/"
    data = {
        'user_name': user,
        'message': text,
    }
    resp = requests.post(url, json=data)
    assert(json.loads(resp.text)['error_code'] == 0)
    count += 1
    print(count, end="\r")

"""
es = Elasticsearch()
bulk = ""
for i, t in enumerate(texts):
    doc = {
        "index": { "_index": "test-index", "_id": str(i) },
    }
    bulk += json.dumps(doc)
    bulk += "\n"
    doc = {
        "message": t,
    }
    bulk += json.dumps(doc)
    bulk += "\n"

print(es.bulk(body=bulk))
es.indices.refresh(index="test-index")

query = {"query": {"match": { "message": "die" }}}
res = es.search(index="test-index", body=query)
for hit in res['hits']['hits']:
    print(hit)
"""
