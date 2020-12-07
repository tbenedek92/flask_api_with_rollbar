from flask import jsonify, Blueprint
import resources.errors as errors
from flask.signals import got_request_exception

bp_error_handler = Blueprint('error_handlers', __name__)

@bp_error_handler.app_errorhandler(errors.UserAlreadyExistError)
@bp_error_handler.app_errorhandler(errors.UserDoesNotExistError)
@bp_error_handler.app_errorhandler(errors.PermissionDenied)
@bp_error_handler.app_errorhandler(errors.EmptyUserList)
def default_error_handler(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    got_request_exception.send(bp_error_handler, exception=error)

    return response