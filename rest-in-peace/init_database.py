import cassandra.cluster
import elasticsearch
import json

import setting

INDEX_TEMPLATE = {
    'mappings': {
        '_source': {
            'includes': [
                'id',
                'room_id',
            ]
        },
        'properties': {
            'id': {
                'type': 'long'
            },
            'room_id': {
                'type': 'long'
            },
            'user_name': {
                'type': 'text'
            },
            'content': {
                'type': 'text',
                'fields': {
                    'lang_analyzed': {
                        'type': 'text',
                        'analyzer': 'english'
                    }
                }
            }
        }
    }
}

def init_database():
    es = elasticsearch.Elasticsearch(setting.ES_HOSTS)
    indexes = elasticsearch.client.IndicesClient(es)
    if not indexes.exists(setting.INDEX_NAME):
        indexes.create(index=setting.INDEX_NAME, body=INDEX_TEMPLATE)

    cluster = cassandra.cluster.Cluster(setting.CASSANDRA_HOSTS)
    session = cluster.connect()
    session.execute("create keyspace if not exists chat with replication = {'class':'SimpleStrategy','replication_factor':1};")
    session.execute("""
create table if not exists chat.messages (
    id bigint, 
    content varchar,
    room_id int,
    user_name varchar,
    primary key ((room_id), id))
    with clustering order by (id desc);""")

init_database()
