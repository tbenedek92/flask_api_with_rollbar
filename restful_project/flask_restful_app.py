from flask import Flask, got_request_exception, Request
import os
import rollbar.contrib.flask as rb_flask
import rollbar
import git
import threading
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from restful_project.restful_resources.errors import errors
from restful_project.restful_resources.routes import initialize_routes



app = Flask(__name__)
api = Api(app, errors=errors)
app.config.setdefault('JWT_SECRET_KEY', 'goX3LAcMwR8AuAyGUVGvfPrEwJgxWtvA9hf2NA4P7J7kV27fx')
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
initialize_routes(api)

def get_git_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=4)
    print(f'Git short sha: {short_sha}')
    return short_sha


@app.before_first_request
def init_rollbar():
    rollbar.init(
        access_token='67e198a2a8134062aa5677967e33d9a5',
        environment='flask_test',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basics_config=False,
        code_version=get_git_sha()
    )
    rollbar.report_message('Rollbar initialized succesfully', level='debug')

    got_request_exception.connect(rb_flask.report_exception, app)


class CustomRequest(Request):

    DEFAULT_RB_ID = 0
    DEFAULT_RB_USERNAME= 'default_test_rollbar_user'
    DEFAULT_RB_EMAIL = 'default_test@rollbar.com'

    @property
    def rollbar_person(self, rb_id=DEFAULT_RB_ID, username=DEFAULT_RB_USERNAME, email=DEFAULT_RB_USERNAME):
        return {'id': rb_id, 'username': username, 'email': email}


@app.route('/')
def hello():
    print("in hello")

    return "Hello World!"


import auto_test

if __name__ == '__main__':
    app.request_class = CustomRequest

    threading.Thread(target=auto_test.auto_test_run).start()
    app.run()
    # from .auto_test.auto_test import auto_test_run
    # auto_test_run()

