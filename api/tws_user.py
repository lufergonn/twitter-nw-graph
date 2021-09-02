from urllib.parse import quote
import json
from typing import Dict

from api.base import get_tws

def tws_user(user: str, ctexact: str = None, mention: str = None, hashtag: str = None) -> Dict:
    ctexact = f'+%22{quote(ctexact)}%22' if ctexact else ''
    mention = f'+%40{mention}' if mention else ''
    hashtag = f'+%23{hashtag}' if hashtag else ''
    
    url = f'https://api.twitter.com/1.1/search/tweets.json?q=from:{user}{ctexact}{mention}'
    url += f'{hashtag}&result_type=recent&count=100'

    data = get_tws(url)
    
    if data != 'error' and len(data['statuses']) > 0:
        tws = []
        for tw in data['statuses']:
            if tw.get('retweeted_status', 0) != 0:
                twtmp = {
                    'user': tw['retweeted_status']['user']['screen_name'],
                    'img': tw['retweeted_status']['user']['profile_image_url_https']
                }
                tws.append(twtmp)
        
        data = {
            'user': data['statuses'][0]['user']['screen_name'],
            'img': data['statuses'][0]['user']['profile_image_url_https'],
            'tws': tws
        }

        data_json = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
        with open(f'data/tws/{user.lower()}.json', 'w', encoding='utf8') as file:
            file.write(data_json)

    return data