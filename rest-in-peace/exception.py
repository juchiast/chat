import traceback
from functools import wraps
from flask import jsonify


def error_response(msg):
    return jsonify({"error_code": 1, "error_message": msg}), 400


def success_response(key=None, value=None):
    if not key:
        return jsonify({"error_code": 0}), 200
    return jsonify({"error_code": 0, key: value}), 200


def catch_panic():
    def _decorator(func):
        @wraps(func)
        def __decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()
                return error_response("{type}: {detail}".format(
                    type=type(e).__name__,
                    detail=str(e)
                ))
        return __decorator
    return _decorator
