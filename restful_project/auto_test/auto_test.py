import requests
import json
import pandas as pd

USERS = pd.DataFrame(columns=['user', 'email', 'password', 'new_password'])
USERS = pd.read_csv('test_data.csv')
URL = 'http://127.0.0.1:5000/'

ENDPOINT_LIST = ['signup', 'login', 'users', 'user']


def Main():
    signup = api_test(ENDPOINT_LIST[0], USERS)
    return


def api_test(endpoint, users=USERS):

    url = URL+endpoint
    headers = {'Content-Type': 'application/json'}
    response = {}
    for index, user in users.iterrows():
        usr = user['user']
        email = user['email']
        pw = user['password']
        new_pw = user['new_password']

        payload = {
                    "user": usr,
                    "email": email,
                    "password": pw,
                    "new_password": new_pw
                    }
        response[index] = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        print(response[index].text)

    return response

if __name__ == '__main__':
    Main()