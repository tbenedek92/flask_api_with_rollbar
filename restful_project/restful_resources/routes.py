from .users import UsersApi, SignupApi, AuthApi, PasswordChangeUserName, PasswordChangeUserID, UserDetailsApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/users')
    api.add_resource(SignupApi, '/signup')
    api.add_resource(PasswordChangeUserName, '/user_name/<user>')
    api.add_resource(PasswordChangeUserID, '/user_id/<id>')
    api.add_resource(UserDetailsApi, '/user_details/<id>')

    api.add_resource(AuthApi, '/login')