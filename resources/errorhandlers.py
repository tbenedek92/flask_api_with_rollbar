import sys
sys.path.append("../")
from flask_main import app
from flask import jsonify
from .errors import UserAlreadyExistError, UserDoesNotExistError, PermissionDenied

@app.errorhandler(UserAlreadyExistError)
def handle_user_already_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(UserDoesNotExistError)
def handle_user_already_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(PermissionDenied)
def handle_user_already_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response