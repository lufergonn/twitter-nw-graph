import pandas as pd
import json
import os

def read_data():
    users = pd.DataFrame(columns=['id', 'img'])
    users_rel = pd.DataFrame(columns=['from', 'to'])

    if os.path.exists('data/rt_users.json'):
        data = open('data/rt_users.json', 'r', encoding='utf8')
        data = json.load(data)
        users = users.append({
            'id': data['user'],
            'img': data['img']
        }, ignore_index=True)

        for rt in data['rts']:
            users = users.append({
                'id': rt['user'],
                'img': rt['img']
            }, ignore_index=True)
            users_rel = users_rel.append({
                'from': data['user'], 
                'to': rt['user']
            }, ignore_index=True)
    
    if os.path.exists('data/tws/'):
        for file in os.listdir('data/tws/'):
            data = open(f'data/tws/{file}', 'r', encoding='utf8')
            data = json.load(data)
            users = users.append({
                'id': data['user'],
                'img': data['img']
            }, ignore_index=True)
            
            for rt in data['tws']:
                users = users.append({
                    'id': rt['user'],
                    'img': rt['img']
                }, ignore_index=True)
                users_rel = users_rel.append({
                    'from': data['user'], 
                    'to': rt['user']
                }, ignore_index=True)

    users = users.drop_duplicates(ignore_index=True)
    users_rel = users_rel.drop_duplicates(ignore_index=True)
    users.to_json('data/users.json', orient='records')
    users_rel.to_json('data/users_rel.json', orient='records')
    return 0

def data_format(user):
    read_data()

    data = {
        'nodes': json.load(open('data/users.json', 'r', encoding='utf8')),
        'edges': json.load(open('data/users_rel.json', 'r', encoding='utf8'))
    }
    data['nodes'] = [{'id': i['id'], 'height': 40, 'fill': {'src': i['img']}} for i in data['nodes']] 
    data = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
    data = f'let data = {data}'

    with open('static/data/arychart.js', 'w', encoding='utf8') as file:
        file.write(data)