from flask import Flask
import os
import rollbar.contrib.flask as rb_flask
from flask import got_request_exception
from flask import Request
import rollbar
import git
from blueprint_project.blueprint_resources.users import user_mgmt
from blueprint_project.blueprint_resources.errorhandlers import bp_error_handler

app = Flask(__name__)


def get_git_sha():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=4)
    print(f'Git short sha: {short_sha}')
    return short_sha


@app.before_first_request
def init_rollbar():
    rollbar.init(
        access_token='8026b336e7e4475482765f8b119d4049',
        environment='flask_test',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basics_config=False,
        code_version=get_git_sha()
    )
    rollbar.report_message('Rollbar initialized succesfully', level='debug')

    got_request_exception.connect(rb_flask.report_exception, app)
    got_request_exception.connect(rb_flask.report_exception, bp_error_handler)


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


if __name__ == '__main__':
    app.request_class = CustomRequest

    app.register_blueprint(user_mgmt)
    app.register_blueprint(bp_error_handler)

    app.run()

