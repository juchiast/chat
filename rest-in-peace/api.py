import cassandra.cluster
from flask import Flask, request

from exception import catch_panic
from model import MessageIdFactory
from routine import get_worker_id


worker_id = get_worker_id()
msg_factory = MessageIdFactory(worker_id)
app = Flask(__name__)
cluster = cassandra.cluster.Cluster()


@app.route("/ping", methods=["GET"])
@catch_panic()
def ping():
    return {"message": "pong"}


@app.route("/<int:room_id>/", methods=["GET"])
@catch_panic()
def load_messages(room_id):
    limit = int(request.args.get('limit'))
    before = request.args.get('before')
    session = cluster.connect('chat')
    rows = None
    if before == None:
        rows = session.execute("select user_name, id, content from messages where room_id=%s order by id desc limit %s" % (room_id, limit))
    else:
        before = int(before)
        rows = session.execute("select user_name, id, content from messages where room_id=%s and id<%s order by id desc limit %s" % (room_id, before, limit))
    res = []
    for row in rows:
        res.append({
            "id": str(row[1]),
            "user_name": row[0],
            "content": row[2],
            "timestamp": msg_factory.get_timestamp_from_id(row[1])
        })
    return {"messages": res}


@app.route("/<int:room_id>/", methods=["POST"])
@catch_panic()
def send_message(room_id):
    body = request.json
    user_name = str(body["user_name"])
    message = str(body["message"])
    session = cluster.connect('chat')
    msg_id = msg_factory.generate_message_id()
    session.execute("insert into messages (id, content, user_name, room_id) values (%s, %s, %s, %s)", (msg_id, message, user_name, room_id))
    return {}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
