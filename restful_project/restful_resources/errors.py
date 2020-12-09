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
        "status": 405
    },
    "UserAlreadyExistError": {
        "message": "User is already in the database, please use PUT method to modify.",
        "status": 405
    },
    "UserDoesNotExistError": {
        "message": "User not found.",
        "status": 405
    },
    "PermissionDenied": {
        "message": "Password mismatch - no permission to update user.",
        "status": 401
    }
}
