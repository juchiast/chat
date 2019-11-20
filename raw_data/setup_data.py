# Insert to Cassandra and Elasticsearch
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()
import json

import make_subtitles

texts = make_subtitles.get_all_texts()
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
