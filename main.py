import os
import json
import time
import asyncio
import argparse
from legym import Legym
from utils import Logger
from datetime import datetime


weekday = datetime.now().weekday()

absdir = os.path.dirname(os.path.abspath(__file__))

loop = asyncio.get_event_loop()

with open(absdir+'/user_info.json', 'r') as f:
    user_info = json.load(f)

with open(absdir+'/activity_list.json', 'r') as f:
    activity_list = json.load(f)

def signup(cancel=False):
    week = (weekday+2)%7
    week = 5
    try:
        tasks = [signup_coro(Legym(user_info[k]), week, v, cancel) for k, v in activity_list[str(week)].items()]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        pass

def checkin(endtime):
    try:
        tasks = [checkin_coro(Legym(user_info[k]), endtime) for k in activity_list[str(weekday+1)].keys()]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        pass

async def signup_coro(user, week, activities, cancel):
    r = await user.login()
    if not r:
        print('Login failed')
        return
    cnt = 0
    while True:
        r = await user.activity_signup(week, activities, cancel)
        for i in r:
            logger.log(user.real_name+'\t'+str(i))
            if '成功' in i['data']['reason'] or '上限' in i['data']['reason']:
                cnt += 1
        if cnt == len(r):
            break
        cnt = 0

async def checkin_coro(user, endtime):
    r = await user.login()
    if not r:
        print('Login failed')
        return
    starttime = datetime.now().strftime("%H%M")
    now = starttime
    while now >= starttime and now < endtime:
        try:
            r = await user.activity_checkin()
            for i in r:
                if i:
                    logger.log(user.real_name+'\t'+str(i))
        except Exception:
            pass
        await asyncio.sleep(30)
        now = datetime.now().strftime("%H%M")


if __name__ == '__main__':
    paser = argparse.ArgumentParser()
    paser.add_argument('action', help='signup or checkin')
    paser.add_argument('-e', '--endtime', help='end time for checkin loop')
    paser.add_argument('-d', '--delay', help='script delay time', type=int, default=0)
    paser.add_argument('-c', '--cancel', help='whether to cancel signup', action='store_true')
    args = paser.parse_args()
    logger = Logger(args.action, absdir+'/log')

    if args.action == 'checkin':
        if not args.endtime:
            print('please specify -e')
            exit(2)
        elif len(args.endtime) != 4:
            print('wrong format for -e')
            exit(2)
        if args.delay:
            time.sleep(args.delay)
        checkin(args.endtime)
    elif args.action == 'signup':
        if args.delay:
            time.sleep(args.delay)
        signup(args.cancel)
