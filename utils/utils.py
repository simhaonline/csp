import time
from datetime import datetime
import json
import requests
import random


def gen_ut_id():
    now = datetime.now()
    second = now.hour * 3600 + now.minute * 60 + now.second
    return int('{}{:0>2}{:0>2}{:0>5}{:0>3}'.format(now.year, now.month, now.day, second, random.randint(0, 999)))


def send_notification(msg='您有新的提醒'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ZWNkMWEwYjkzOGUyODE0OGY4ZjMwNmJiOjY2YmZkYjA5NTVjMzQ1Mjc2YmIxYmI5Yw=='
    }
    url = 'https://api.jpush.cn/v3/push'
    r = requests.post(url, headers=headers, data=json.dumps({
        'platform': 'all',
        'audience': 'all',
        'notification': {
            'alert': msg
        }
    }))
    print(r.text)


if __name__ == '__main__':
    print(gen_ut_id())
