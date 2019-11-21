import cassandra.cluster

import setting
from model import MessageIdFactory


def get_worker_id():
    # TODO:
    # Implement ID counter in Redis
    # https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html
    return 1


cluster = cassandra.cluster.Cluster()
session = cluster.connect(setting.APP_NAME)
worker_id = get_worker_id()
msg_factory = MessageIdFactory(worker_id)


def load_messages(room_id, limit, before=None):
    before_condition = 'and id<{} '.format(int(before)) if before else ''
    rows = session.execute(
        "select user_name, id, content "
        "from messages "
        "where room_id={room} {extend_condition}"
        "order by id desc limit {limit}".format(
            room=room_id,
            limit=limit,
            extend_condition=before_condition
        )
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
        "values ({id}, {message}, {user}, {room})".format(
            id=msg_id,
            message=message,
            user=user_name,
            room=room_id,
        )
    )
