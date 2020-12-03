from flask import Flask, jsonify, request
import os
import rollbar.contrib.flask as rb_flask
from flask import got_request_exception
from flask import Request
import pandas as pd
from flask_restful import reqparse
import rollbar
import resources.errors as errors

app = Flask(__name__)

@app.before_first_request
def init_rollbar():
    rollbar.init(
        access_token='8026b336e7e4475482765f8b119d4049',
        environment='flask_test',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basics_config=False
    )
    rollbar.report_message('Rollbar initialized succesfully', level='debug')

    got_request_exception.connect(rb_flask.report_exception, app)


class CustomRequest(Request):
    @property
    def rollbar_person(self):
        return {'id': '0', 'username':'test_user', 'email': 'test_user@example.com'}

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


@app.route('/user', methods=['POST'])
def add_user():
    global user_df
    global parser

    args = parser.parse_args()
    user = args['user']
    pw = args['password']
    if user not in user_df['user'].values:
        user_dict = {'user': user,
                     'pw': pw}
        user_df = user_df.append(user_dict, ignore_index=True)
        print(user_df)
        return jsonify(user_dict), 201
    else:
        raise errors.UserAlreadyExistError("user is already in the database, please use PUT method")


@app.route('/user/<string:user>', methods=['PUT'])
def update_user(user):
    global user_df
    global parser

    args = parser.parse_args()
    # user = args['user']
    pw = args['password']
    new_pw = args['new_password']

    if user in user_df['user'].values:
        user_dict = {'user': user,
                     'pw': new_pw}
        if user_df[user_df['user'] == user]['pw'][0] == pw:

            user_df.at[user_df[user_df['user'] == user].index.min(), 'pw'] = new_pw
            print(user_df)
            return jsonify(user_dict), 201
        else:
            raise errors.PermissionDenied("Password mismatch - no permission to update user")
    else:
        raise errors.UserDoesNotExistError("user not found")


@app.route('/user', methods=['DELETE'])
def delete_user():

    return None


def Main():
    global user_df
    global parser

    user_df = pd.DataFrame(columns=['user', 'pw'])
    parser = reqparse.RequestParser()
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('new_password')


if __name__ == '__main__':
    Main()
    app.run()

