from flask import Blueprint, jsonify
from flask_restful import reqparse
import pandas as pd
import resources.errors as errors


user_mgmt = Blueprint('user_mgmt', __name__)
user_df = pd.DataFrame(columns=['user', 'pw'])
parser = reqparse.RequestParser()
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('new_password')


@user_mgmt.route('/user', methods=['POST'])
def add_user():
    global user_df

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


@user_mgmt.route('/user/<string:user>', methods=['PUT'])
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
        min_index = user_df[user_df['user'] == user].index.min()
        if user_df[user_df['user'] == user]['pw'][min_index] == pw:

            user_df.at[min_index, 'pw'] = new_pw
            print(user_df)
            return jsonify(user_dict), 201
        else:
            raise errors.PermissionDenied("Password mismatch - no permission to update user")
    else:
        raise errors.UserDoesNotExistError("user not found")




@user_mgmt.route('/userlist', methods=['GET'])
def get_user_list():
    if len(user_df) > 0:
        user_list = user_df['user'].tolist()
        return jsonify(user_list), 201
    else:
        raise errors.EmptyUserList("No user has been registered yet")

@user_mgmt.route('/user', methods=['DELETE'])
def delete_user():

    return None