from .users import UsersApi, SignupApi, AuthApi, UserApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/users')
    api.add_resource(SignupApi, '/signup')
    api.add_resource(UserApi, '/user/<user>')
    api.add_resource(AuthApi, '/login')