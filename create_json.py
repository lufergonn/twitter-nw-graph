from api.tws_user import tws_user
import numpy as np
import json
import os
import time

def get_users_to_create():
    dir_tws = 'data/tws'
    ls = os.listdir(dir_tws)

    files = []
    for file in ls:
        data = open(f'{dir_tws}/{file}', 'r', encoding='utf8')
        data = json.load(data)
        data = [tw['rt']['user'].lower() for tw in data['tws'] if tw.get('rt', 0) != 0]
        data = [user for user in data if f'{user}.json' not in ls]
        files += data
    
    if os.path.exists('data/rt_users.json'):
        data = open('data/rt_users.json', 'r', encoding='utf8')
        data = json.load(data)
        data = [tw['user'] for tw in data['rts'] if tw['user'] not in ls]
        files += data

    files = np.unique(files)
    return files

def create_json():
    users = get_users_to_create()
    count = 0

    for user in users:
        time.sleep(5)
        msg = tws_user(user)
        if msg == 'error':
            print(f'[...] ---> Error [ {user} ]')
            print(users)
            break
        
        print(f'[...] ---> Saved data of [ {user} ]')
        count += 1

    return count
