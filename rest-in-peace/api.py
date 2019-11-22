from flask import Flask, request

from wrap_response import wrap_response
from routine import load_messages, send_message

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
@wrap_response()
def ping_api():
    return {"message": "pong"}


@app.route("/<int:room_id>/", methods=["GET"])
@wrap_response()
def load_messages_api(room_id):
    limit = int(request.args.get('limit'))
    before = request.args.get('before')
    return {"messages": load_messages(room_id, limit, before)}


@app.route("/<int:room_id>/", methods=["POST"])
@wrap_response()
def send_message_api(room_id):
    body = request.json
    user_name = str(body["user_name"])
    message = str(body["message"])
    send_message(room_id, user_name, message)
    return {}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
