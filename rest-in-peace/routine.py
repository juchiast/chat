import cassandra.cluster
import elasticsearch
import json
import time
import redis

import setting


def get_worker_id():
    r = redis.Redis(setting.REDIS_HOST)
    return r.incr('worker_count') % (1 << 10)


def get_timestamp_from_id(id):
    return id >> 31


class IdGenerator:
    def __init__(self):
        self.worker_id = get_worker_id()
        self.count = 0

    def next_id(self):
        self.count += 1
        timestamp = int(time.time())
        # 63-bit id:
        # 32-bit timestamp, 10-bit worker's id, 21-bit local counter
        return (timestamp << 31) | (self.worker_id << 21) | (self.count % (1 << 21))


cluster = cassandra.cluster.Cluster(setting.CASSANDRA_HOSTS)
session = cluster.connect(setting.KEYSPACE_NAME)
id_generator = IdGenerator()
es = elasticsearch.Elasticsearch(setting.ES_HOSTS)
re = redis.Redis()


def load_messages(room_id, limit, before):
    if before == None:
        rows = session.execute(
            "select user_name, id, content "
            "from messages "
            "where room_id=%s "
            "order by id desc limit %s ",
            (room_id, limit)
        )
    else:
        before = int(before)
        rows = session.execute(
            "select user_name, id, content "
            "from messages "
            "where room_id=%s and id<%s "
            "order by id desc limit %s ",
            (room_id, before, limit)
        )
    messages = []
    for row in rows:
        row_id = row[1]
        messages.append({
            "id": str(row_id),
            "user_name": row[0],
            "content": row[2],
            "timestamp": get_timestamp_from_id(row_id)
        })
    return messages


def send_message(room_id, user_name, message):
    msg = {
        'id': id_generator.next_id(),
        'content': message,
        'room_id': room_id,
        'user_name': user_name,
    }
    re.publish('new_messages', json.dumps(msg))


def search(room_id, query):
    q = {
        '_source': ['id'],
        'sort': [{'id': 'desc'}],
        'query': {
            'bool': {
                'must': [
                    {'match': {'content': query}},
                ],
                'filter': [
                    {'term': {'room_id': room_id}},
                ],
            },
        },
    }
    resp = es.search(index=setting.INDEX_NAME, body=q)
    ids = (x['_source']['id'] for x in resp['hits']['hits'])
    result = []
    for msg_id in ids:
        row = session.execute(
            "select user_name, content "
            "from messages "
            "where room_id=%s and id=%s ",
            (room_id, msg_id)
        )[0]
        result.append({
            'id': str(msg_id),
            'user_name': row[0],
            'content': row[1],
            'timestamp': get_timestamp_from_id(msg_id),
        })
    return result
