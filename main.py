import os
import json
import asyncio
import argparse
from legym import Legym
from utils import Logger
from datetime import datetime


def signup(endtime, cancel=False):
    week = (weekday+2)%7
    tasks = [[loop.create_task(signup_coro(Legym(user_info[j]), week, i['activities'], cancel, endtime)) for j in i['users']] for i in activity_list[str(week)]][0]
    loop.run_until_complete(asyncio.wait(tasks))

def checkin(endtime):
    week = (weekday+1)%7
    tasks = [loop.create_task(checkin_coro(Legym(user_info[j]), endtime)) for i in [a['users'] for a in activity_list[str(week)]] for j in i]
    loop.run_until_complete(asyncio.wait(tasks))

async def signup_coro(user, week, activities, cancel, endtime):
    r = await user.login()
    if not r:
        raise Exception('Login failed')
    await asyncio.sleep(args.delay)
    cnt = 0
    starttime = datetime.now().strftime("%H%M")
    now = starttime
    while now >= starttime and now < endtime:
        try:
            r = await user.activity_signup(week, activities, cancel)
            for i in r:
                if '未开始' not in i['data']['reason'] and '已结束' not in i['data']['reason'] and '已经满' not in i['data']['reason'] and '上限' not in i['data']['reason']:
                    logger.log(user.student_id+' '+str(i))
                if '成功' in i['data']['reason'] or '上限' in i['data']['reason']:
                    cnt += 1
            if cnt == len(r):
                break
            cnt = 0
        except Exception as e:
            print(e)
            errlogger.log(str(e))
            print('retrying...')
            await user.login()

async def checkin_coro(user, endtime):
    r = await user.login()
    if not r:
        raise Exception('Login failed')
    await asyncio.sleep(args.delay)
    starttime = datetime.now().strftime("%H%M")
    now = starttime
    while now >= starttime and now < endtime:
        try:
            r = await user.activity_checkin()
            for i in r:
                if '成功' in i['message']:
                    logger.log(user.student_id+' '+str(i))
            await asyncio.sleep(15)
            now = datetime.now().strftime("%H%M")
        except Exception as e:
            print(e)
            errlogger.log(str(e))
            print('retrying...')
            await user.login()


if __name__ == '__main__':
    paser = argparse.ArgumentParser()
    paser.add_argument('action', help='signup or checkin')
    paser.add_argument('-e', '--endtime', help='end time for an action loop (0000-2400)')
    paser.add_argument('-d', '--delay', help='script delay time (in seconds)', type=int, default=0)
    paser.add_argument('-c', '--cancel', help='cancel signup', action='store_true')
    args = paser.parse_args()

    weekday = datetime.now().weekday()
    absdir = os.path.dirname(os.path.abspath(__file__))
    logger = Logger(args.action, absdir+'/log')
    errlogger = Logger('error', absdir+'/log')
    loop = asyncio.get_event_loop()

    with open(absdir+'/user_info.json', 'r') as f:
        user_info = json.load(f)
    with open(absdir+'/activity_list.json', 'r') as f:
        activity_list = json.load(f)

    if args.endtime:
        if len(args.endtime) != 4:
            print('wrong format for -e')
            os._exit(2)
        try:
            t = int(args.endtime)
            if t < 0 or t > 2400:
                print('invalid time for -e')
                os._exit(2)
        except:
            print('wrong format for -e')
            os._exit(2)
    if args.action == 'checkin':
        if not args.endtime:
            print('please specify -e')
            os._exit(2)
        checkin(args.endtime)
    elif args.action == 'signup':
        signup(args.endtime if args.endtime else '2400', args.cancel)
