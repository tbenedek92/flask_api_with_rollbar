import pandas as pd
from datetime import datetime, timedelta, timezone
import time
import restful_project.restful_resources.errors as errors
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

user_df = pd.DataFrame(columns=['user', 'email', 'password'])
parser = reqparse.RequestParser()
parser.add_argument('user')
parser.add_argument('email')
parser.add_argument('password')
parser.add_argument('new_password')


class UsersApi(Resource):

    @jwt_required
    def get(self):
        if len(user_df) > 0:
            user_dict = user_df[['user', 'email']].to_dict(orient='index')
            print(user_dict)
            return user_dict, 201
        else:
            raise errors.EmptyUserList

    def post(self):
        return


def check_password(password_hash, password):
    return check_password_hash(password_hash, password)


def hash_password(password):
    return generate_password_hash(password).decode('utf8')


class SignupApi(Resource):

    def post(self):
        global user_df

        args = parser.parse_args()
        user = args['user']
        email = args['email']
        password = hash_password(args['password'])

        if user not in user_df['user'].values:
            user_dict = {'user': user,
                         'email': email,
                         'password': password}
            user_df = user_df.append(user_dict, ignore_index=True)
            user_id = user_df[user_df['email'] == email].index.min()
            user_dict['id'] = int(user_id)
            print(user_df)

            return user_dict, 201
        else:
            raise errors.UserAlreadyExistError("user is already in the database, please use PUT method")


class AuthApi(Resource):

    def post(self):

        global user_df

        args = parser.parse_args()
        user = args['user']
        password = args['password']

        selected_user = user_df[user_df['user']==user]

        if len(selected_user)>0:
            selected_user_index=int(selected_user.index.min())
            password_hash = selected_user['password'][selected_user_index]
            authorized = check_password(password_hash, password)

            if authorized:
                acs_token = {}
                delta = timedelta(hours=4)

                acs_token['valid_to'] = (datetime.utcnow()+delta).replace(tzinfo=timezone.utc).timestamp()
                acs_token['token'] = create_access_token(identity=selected_user_index, expires_delta=delta)
                return acs_token, 200
            else:
                raise errors.PermissionDenied
        else:
            raise errors.EmptyUserList


class UserApi(Resource):

    @jwt_required
    def put(self, user):
        global user_df
        user_id = get_jwt_identity()
        print(user_id)
        args = parser.parse_args()
        # user = args['user']
        password = args['password']
        new_password = args['new_password']

        if user in user_df['user'].values:
            user_dict = {'user': user,
                         'password': new_password}
            min_index = user_df[user_df['user'] == user].index.min()
            if min_index == user_id:

                user_df.at[min_index, 'password'] = hash_password(new_password)
                print(user_df)
                return {'response': 'Password succesfully updated'}, 201
            else:
                raise errors.PermissionDenied
        else:
            raise errors.UserDoesNotExistError("user not found")

def add_user():
    global user_df

    args = parser.parse_args()
    user = args['user']
    password = args['password']
    if user not in user_df['user'].values:
        user_dict = {'user': user,
                     'password': password}
        user_df = user_df.append(user_dict, ignore_index=True)
        print(user_df)
        return jsonify(user_dict), 201
    else:
        raise errors.UserAlreadyExistError("user is already in the database, please use PUT method")


def update_user(user):
    global user_df
    global parser

    args = parser.parse_args()
    # user = args['user']
    password = args['password']
    new_password = args['new_password']

    if user in user_df['user'].values:
        user_dict = {'user': user,
                     'password': new_password}
        min_index = user_df[user_df['user'] == user].index.min()
        if user_df[user_df['user'] == user]['password'][min_index] == password:

            user_df.at[min_index, 'password'] = new_password
            print(user_df)
            return jsonify(user_dict), 201
        else:
            raise errors.PermissionDenied("Password mismatch - no permission to update user")
    else:
        raise errors.UserDoesNotExistError("user not found")




def get_user_list():
    if len(user_df) > 0:
        user_list = user_df['user'].tolist()
        return jsonify(user_list), 201
    else:
        raise errors.EmptyUserList("No user has been registered yet")

def delete_user():

    return None