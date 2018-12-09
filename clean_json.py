import json
import re

with open('tweets_raw.json') as f:
    tweets = json.load(f)

new = []

for tweet in tweets:
    temp = {}
    temp['full_text'] = re.sub(' https://t.co/\w+$', '', tweet['full_text'])
    temp['created_at'] = tweet['created_at']
    temp['media_url_https'] = tweet['extended_entities']['media'][0]['media_url_https']
    new.append(temp)

with open('output.json', 'w') as outfile:
    json.dump(new, outfile)
