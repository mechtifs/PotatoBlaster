import os
import json
import time
import asyncio
import argparse
from legym import Legym
from utils import Logger
from datetime import datetime


def signup(cancel=False):
    week = (weekday+2)%7
    try:
        tasks = [[signup_coro(Legym(user_info[j]), week, i[1], cancel) for j in i[0]] for i in [(a['users'], a['activities']) for a in activity_list[str(week)]]][0]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        pass

def checkin(endtime):
    week = (weekday+1)%7
    try:
        tasks = [checkin_coro(Legym(user_info[j]), endtime) for i in [a['users'] for a in activity_list[str(week)]] for j in i]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception:
        pass

async def signup_coro(user, week, activities, cancel):
    r = await user.login()
    if not r:
        print('Login failed')
        return
    await asyncio.sleep(args.delay)
    cnt = 0
    while True:
        r = await user.activity_signup(week, activities, cancel)
        for i in r:
            logger.log(user.student_id+' '+str(i))
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
    await asyncio.sleep(args.delay)
    starttime = datetime.now().strftime("%H%M")
    now = starttime
    while now >= starttime and now < endtime:
        try:
            r = await user.activity_checkin()
            for i in r:
                if i:
                    logger.log(user.student_id+' '+str(i))
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

    weekday = datetime.now().weekday()
    absdir = os.path.dirname(os.path.abspath(__file__))
    logger = Logger(args.action, absdir+'/log')
    loop = asyncio.get_event_loop()

    with open(absdir+'/user_info.json', 'r') as f:
        user_info = json.load(f)
    with open(absdir+'/activity_list.json', 'r') as f:
        activity_list = json.load(f)

    if args.action == 'checkin':
        if not args.endtime:
            print('please specify -e')
            exit(2)
        elif len(args.endtime) != 4:
            print('wrong format for -e')
            exit(2)
        checkin(args.endtime)
    elif args.action == 'signup':
        signup(args.cancel)
