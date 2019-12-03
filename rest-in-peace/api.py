from flask import Flask, request
from flask_cors import CORS
from flask import Response

from wrap_response import wrap_response
from routine import load_messages, send_message, search, get_all, get_search_perf
import routine

app = Flask(__name__)
CORS(app)

@app.route("/api/ping", methods=["GET"])
@wrap_response()
def ping_api():
    return {"message": "pong"}


@app.route("/api/<int:room_id>/", methods=["GET"])
@wrap_response()
def load_messages_api(room_id):
    limit = int(request.args.get('limit'))
    before = request.args.get('before')
    return {"messages": load_messages(room_id, limit, before)}


@app.route("/api/<int:room_id>/", methods=["POST"])
@wrap_response()
def send_message_api(room_id):
    body = request.json
    user_name = str(body["user_name"])
    message = str(body["message"])
    send_message(room_id, user_name, message)
    return {}


@app.route("/api/<int:room_id>/search/", methods=["POST"])
@wrap_response()
def search_api(room_id):
    body = request.json
    query = str(body['query'])
    return {'messages': search(room_id, query)}


@app.route("/api/get_all/", methods=["GET"])
def get_all_api():
    return Response(get_all(), mimetype='text/csv')


@app.route("/api/get_search_perf/", methods=["GET"])
def get_search_perf_api():
    return Response(get_search_perf(), mimetype='text/csv')


@app.route("/api/")
def example_client():
    return open('./example_client.html', 'r').read()
