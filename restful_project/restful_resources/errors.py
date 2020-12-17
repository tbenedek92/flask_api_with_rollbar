class UserAlreadyExistError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class PermissionDenied(PermissionError):
    pass


class EmptyUserList(Exception):
    pass


errors = {
    "EmptyUserList": {
        "message": "No user has been registered yet.",
        "status": 405,
    },
    "UserAlreadyExistError": {
        "message": "User is already in the database, please use PUT method to modify.",
        "status": 405,
    },
    "UserDoesNotExistError": {
        "message": "User not found.",
        "status": 405,
    },
    "PermissionDenied": {
        "message": "Permission denied - You are not authorized to perform this action",
        "status": 401,
    }
}


def custom_exception_handler(payload):
    exception_class = None
    try:
        exception_class = payload['data']['body']['trace']['exception']['class']
    except KeyError:
        pass

    if exception_class is not None and exception_class in errors.keys():
        payload['data']['level'] = 'info'

    return payload
