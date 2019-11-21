import traceback
import cassandra.cluster
from flask import Flask, request, jsonify
from functools import wraps

from model import MessageIdFactory
from routine import get_worker_id


worker_id = get_worker_id()
msg_factory = MessageIdFactory(worker_id)


def error_response(msg):
    return jsonify({"error_code": 1, "error_message": msg}), 400


def success_response(key=None, value=None):
    if key == None:
        return jsonify({"error_code": 0}), 200
    return jsonify({"error_code": 0, key: value}), 200


def catch_panic():
    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                return error_response("%s: %s" % (type(e).__name__, str(e)))
        return __decorator
    return _decorator


app = Flask(__name__)
cluster = cassandra.cluster.Cluster()


@app.route("/ping", methods=["GET"])
@catch_panic()
def ping():
    return "pong"


@app.route("/<int:room_id>/", methods=["GET"])
@catch_panic()
def load_messages(room_id):
    limit = int(request.args.get('limit'))
    before = request.args.get('before')
    session = cluster.connect('chat')
    rows = session.execute("select user_name, id, content from messages where room_id=%s order by id desc limit %s" % (room_id, limit))
    res = []
    for row in rows:
        res.append({
            "id": str(row[1]),
            "user_name": row[0],
            "content": row[2],
            "timestamp": msg_factory.get_timestamp_from_id(row[1])
        })
    return success_response("messages", res)


@app.route("/<int:room_id>/", methods=["POST"])
@catch_panic()
def send_message(room_id):
    body = request.json
    user_name = str(body["user_name"])
    message = str(body["message"])
    session = cluster.connect('chat')
    msg_id = msg_factory.generate_message_id()
    session.execute("insert into messages (id, content, user_name, room_id) values (%s, %s, %s, %s)", (msg_id, message, user_name, room_id))
    return success_response()


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
