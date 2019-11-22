import cassandra.cluster
import elasticsearch
import json

import setting
from model import MessageIdFactory


def get_worker_id():
    # TODO:
    # Implement ID counter in Redis
    # https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html
    return 1


cluster = cassandra.cluster.Cluster()
session = cluster.connect(setting.KEYSPACE_NAME)
worker_id = get_worker_id()
msg_factory = MessageIdFactory(worker_id)
es = elasticsearch.Elasticsearch()


def load_messages(room_id, limit, before=None):
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
            "timestamp": msg_factory.get_timestamp_from_id(row_id)
        })
    return messages


def send_message(room_id, user_name, message):
    msg_id = msg_factory.generate_message_id()
    session.execute(
        "insert into messages (id, content, user_name, room_id) "
        "values (%s, %s, %s, %s) ",
        (msg_id, message, user_name, room_id)
    )
    msg = {
        'id': msg_id,
        'content': message,
        'room_id': room_id,
        'user_name': user_name,
    }
    resp = es.index(index=setting.INDEX_NAME, body=msg)
    assert(resp['result'] == 'created')
