# Insert to Cassandra and Elasticsearch
import json
from elasticsearch import Elasticsearch
import make_subtitles

es = Elasticsearch()

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
