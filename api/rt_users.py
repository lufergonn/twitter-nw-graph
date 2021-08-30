import json
from api.base import get_tws

def rt_users(id):
    url = f'https://api.twitter.com/1.1/statuses/retweets/{id}.json?count=100'
    data = get_tws(url)

    if data != 'error' and len(data) > 0:
        rts = []
        for rt in data:
            rttmp = {
                'user': rt['user']['screen_name'],
                'img': rt['user']['profile_image_url_https']
            }
            rts.append(rttmp)
        
        data = {
            'user': data[0]['retweeted_status']['user']['screen_name'],
            'img': data[0]['retweeted_status']['user']['profile_image_url_https'],
            'rts': rts
        }

        data_json = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
        with open('data/rt_users.json', 'w', encoding='utf8') as file:
            file.write(data_json)

    return data