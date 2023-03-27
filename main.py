import os
import json
import time
import argparse
import threading
from legym import Legym
from utils import Logger
from datetime import datetime


weekday = datetime.now().weekday()

absdir = os.path.dirname(os.path.abspath(__file__))

with open(absdir+'/user_info.json', 'r') as f:
    user_info = json.load(f)

with open(absdir+'/activity_list.json', 'r') as f:
    activity_list = json.load(f)

def checkin(endtime):
    for k in activity_list[str(weekday+1)].keys():
        try:
            threading.Thread(target=checkin_thread, args=(Legym(user_info[k]), endtime,)).start()
        except Exception:
            print(k, 'wrong password')
            pass

def signup(cancel=False):
    week = (weekday+2)%7
    for k, v in activity_list[str(week)].items():
        try:
            threading.Thread(target=signup_thread, args=(Legym(user_info[k]), week, v, cancel,)).start()
        except Exception:
            print(k, 'wrong password')
            pass

def checkin_thread(user, endtime):
    starttime = datetime.now().strftime("%H%M")
    now = starttime
    while now >= starttime and now < endtime:
        try:
            r = user.activity_check_in()
            for i in r:
                logger.log(user.real_name+'\t'+str(i))
        except Exception:
            pass
        time.sleep(30)
        now = datetime.now().strftime("%H%M")

def signup_thread(user, week, activities, cancel):
    while True:
        r = user.activity_sign_up(week, activities, cancel)
        logger.log(user.real_name+'\t'+str(r))
        if '成功' in r['reason'] or '上限' in r['reason']:
            break


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
