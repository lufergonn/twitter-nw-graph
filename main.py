from api.rt_users import rt_users
from api.tws_user import tws_user
from create_json import create_json
from data_format import data_format
from shutil import rmtree
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', default='tweet',help='Tweet or User')
    parser.add_argument('-v', '--value', default='',
            help='For tweets, tweet id and for users, twitter username.')
    parser.add_argument('-n', '--number-levels', default=1, type=int, help='Number of levels')
    parser.add_argument('-x', '--ctexact', default='',help='[type:user][optional] Containing the exact phrase "x"')
    parser.add_argument('-m', '--mention', default='',help='[type:user][optional] Mentioning Twitter account "x"')
    parser.add_argument('-g', '--hashtag', default='',help='[type:user][optional] Containing the hashtag "x"')

    args = parser.parse_args()
    type_tweet = args.type.lower() if args.type.lower() in ['tweet', 'user'] else False
    value_tweet = args.value if args.value != '' else False
    number_levels = args.number_levels if args.number_levels > 0 else False
    
    if type_tweet and value_tweet and number_levels:
        print('\n\tTwitter-rt-graphnetwork\n\n')
        print('[...] Creating folders / deleting previous used data')
        if os.path.exists('data/tws/'):
            rmtree('data')

        os.makedirs('data/tws', exist_ok=True)

        print(f'[...] Getting level 1 data')
        user = ''
        if type_tweet == 'tweet':
            user = rt_users(value_tweet)
            if len(user) == 0:
                print('\n\tNo tweets\n\n')
                return 1
        else :
            user = tws_user(value_tweet, args.ctexact, args.mention, args.hashtag)
            if user.get('user', 0) == 0:
                print('\n\tNo tweets\n\n')
                return 1

        if user == 'error':
            print('\n\tError\n\n')
            return 0

        user = user['user']
        print(f'[...] ---> Saved data of [ {user} ]')
        
        for i in range(number_levels - 1):
            print(f'[...] Getting level {i + 2} data')
            create_json()
        
        print('[...] Formatting data for charts')
        data_format(user)

        print('\nThe results were saved in ./static/\n\n')
        return 2
    else:
        print('\n\tError\n')
        return 0        

if __name__ == '__main__':
    main()