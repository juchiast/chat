import traceback
from functools import wraps
from flask import jsonify


def error_response(message):
    response_data = {
        "error_code": 1,
        "error_message": message,
    }
    return jsonify(response_data), 400


def success_response(response_data):
    response_data.update({"error_code": 0})
    return jsonify(response_data), 200


def wrap_response():
    def _decorator(func):
        @wraps(func)
        def __decorator(*args, **kwargs):
            try:
                return success_response(func(*args, **kwargs))
            except Exception as e:
                traceback.print_exc()
                return error_response("{type}: {detail}".format(
                    type=type(e).__name__,
                    detail=str(e)
                ))
        return __decorator
    return _decorator
