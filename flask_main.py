from flask import Flask, jsonify, request
import os
import rollbar.contrib.flask as rb_flask
from flask import got_request_exception
from flask import Request
import pandas as pd
from flask_restful import reqparse
import rollbar
import resources.errors as errors
import git
from resources.users import user_mgmt

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



class CustomRequest(Request):
    @property
    def rollbar_person(self):
        return {'id': '0', 'username':'test_rollbar_user', 'email': 'test_rollbar_user@example.com'}

app.request_class = CustomRequest

@app.route('/')
def hello():
    print("in hello")
    x = None
    # try:
    x[5]
    # except:
    #     rollbar.report_exc_info()

    return "Hello World!"





@app.errorhandler(errors.UserAlreadyExistError)
@app.errorhandler(errors.UserDoesNotExistError)
@app.errorhandler(errors.PermissionDenied)
@app.errorhandler(errors.EmptyUserList)
def default_error_handler(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



if __name__ == '__main__':
    app.register_blueprint(user_mgmt)
    app.run()

