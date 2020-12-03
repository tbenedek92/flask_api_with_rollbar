from flask_main import app, errors
from flask import jsonify

@app.errorhandler(errors.UserAlreadyExistError)
def handle_user_already_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(errors.UserDoesNotExistError)
def handle_user_doesnt_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(errors.PermissionDenied)
def handle_permission_denied(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response