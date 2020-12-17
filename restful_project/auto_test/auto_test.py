import requests
import json
import pandas as pd
import random
from time import sleep, time
import threading
import os

if os.path.exists('test_data.csv'):
    TEST_FILE_PATH = 'test_data.csv'
elif os.path.exists('auto_test/test_data.csv'):
    TEST_FILE_PATH = 'auto_test/test_data.csv'
else:
    raise FileExistsError("TEST_FILE_PATH IS INVALID")

USERS = pd.DataFrame(columns=['user', 'email', 'password', 'new_password'])
USERS = pd.read_csv(TEST_FILE_PATH)
URL = 'http://127.0.0.1:5000/'

ENDPOINT_LIST = ['signup', 'login', 'users', 'user']


def auto_test_run():
    sleep(2)
    api_call(ENDPOINT_LIST[0], 'POST', USERS)
    logins = api_call(ENDPOINT_LIST[1], 'POST', USERS)
    token = {}
    for index, login in logins.items():
        resp = json.loads(login.text)
        token[resp['user_id']] = resp['token']




    # generate_useralreadyexist_errors(continous=True)
    return


def get_new_token_thread(logins):
    while 1:
        get_new_token(logins)
        sleep(10)


def get_new_token(logins):
    for login in logins:
        resp = json.loads(login.text)
        if time() > resp['valid_to']-600:
            api_call(f'user_id/{resp["user_id"]}', 'GET')
            logins = api_call(ENDPOINT_LIST[1], 'POST', USERS)
            break
    return logins


def generate_useralreadyexist_errors(runs=10, continous=False, delay='auto'):

    signup_response = {}
    first_run = True
    while continous or first_run:
        if delay == 'auto':
            delay_s = random.randrange(10, 100, 1)
        elif isinstance(delay, int):
            delay_s = delay
        else:
            delay_s = 10
        for i in range(runs):
            signup_response[i] = api_call('signup', 'POST', USERS)
        first_run = False
        print(f'error_generation is sleeping for {delay_s}')
        sleep(delay_s)

    return signup_response


def api_call(endpoint, method, users=USERS, token=None):

    url = URL+endpoint
    headers = get_headers(token)
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
        response[index] = requests.request(method, url, headers=headers, data=json.dumps(payload))

        print(response[index].text)

    return response


def get_headers(token):
    headers = {
        'Content-Type': 'application/json'
    }

    if token is not None:
        headers['Authorization'] = f'Bearer {token}'

    return headers


if __name__ == '__main__':
    auto_test_run()