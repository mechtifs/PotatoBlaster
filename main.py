import sys
import json
import time
import threading
from legym import Legym
from datetime import datetime


weekday = datetime.now().weekday()

with open('user_info.json', 'r') as f:
    user_info = json.load(f)

with open('activity_list.json', 'r') as f:
    activity_list = json.load(f)

def checkin():
    for k in activity_list[str(weekday+1)].keys():
        try:
            threading.Thread(target=checkin_thread, args=(Legym(user_info[k]),)).start()
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

def checkin_thread(user):
    loop = 1
    now = datetime.now().strftime("%H%M")
    while (now > '1750' and now < '1900') or (now > '1920' and now < '2000'):
        print('# Loop '+str(loop)+' start ('+datetime.now().strftime("%H:%M:%S")+')\n')
        try:
            user.activity_check_in()
            time.sleep(10)
        except Exception:
            pass
        print('\n# Loop '+str(loop)+' end\n')
        loop += 1
        time.sleep(30)
        now = datetime.now().strftime("%H%M")

def signup_thread(user, week, activities, cancel):
    while True:
        r = user.activity_sign_up(week, activities, cancel)
        if r['success'] == 'True' or '上限' in r['reason']:
            break
        time.sleep(0.5)


if __name__ == '__main__':
    if sys.argv[1] == 'checkin':
        checkin()
    elif sys.argv[1] == 'signup':
        signup()
    elif sys.argv[1] == 'cancelsignup':
        signup(cancel=True)
