from .users import UserApi, UsersApi, SignupApi, AuthApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/user/<id>')
    api.add_resource(SignupApi, '/signup')
    api.add_resource(AuthApi, '/login')