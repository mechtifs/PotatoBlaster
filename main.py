import sys
import json
import time
from legym import Legym
from datetime import datetime


weekday = datetime.now().weekday()

with open('user_info.json', 'r') as f:
    user_info = json.load(f)

with open('activity_list.json', 'r') as f:
    activity_list = json.load(f)

def checkin():
    users = []
    for k in activity_list[str(weekday+1)].keys():
        try:
            print('Logged in', end=' ')
            users.append(Legym(user_info[k]))
            time.sleep(5)
        except Exception:
            print('-', k, 'wrong password')
            pass
    loop = 1
    now = datetime.now().strftime("%H%M")
    while (now > '1750' and now < '1900') or (now > '1920' and now < '2000'):
        print('# Loop '+str(loop)+' start ('+datetime.now().strftime("%H:%M:%S")+')\n')
        for user in users:
            try:
                user.activityCheckIn()
                time.sleep(10)
            except Exception:
                pass
        print('\n# Loop '+str(loop)+' end\n')
        loop += 1
        time.sleep(30)
        now = datetime.now().strftime("%H%M")

def signup(cancel=False):
    for k, v in activity_list[str((weekday+2)%7)].items():
        try:
            Legym(user_info[k]).activity_sign_up((weekday+2)%7, v, cancel)
        except Exception:
            print(k, 'wrong password')
            pass


if __name__ == '__main__':
    if sys.argv[1] == 'checkin':
        checkin()
    elif sys.argv[1] == 'signup':
        signup()
    elif sys.argv[1] == 'cancelsignup':
        signup(cancel=True)
