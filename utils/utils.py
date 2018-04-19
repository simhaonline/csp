import time
import datetime
import random


def gen_ut_id():
    now = datetime.datetime.now()
    second = now.hour * 3600 + now.minute * 60 + now.second
    return int('{}{:0>2}{:0>2}{:0>5}{}'.format(now.year, now.month, now.day, second, random.randint(0, 999)))


if __name__ == '__main__':
    print(gen_ut_id())
