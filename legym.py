import sys
import json
import time
from datetime import datetime
from api.base import login, getSemesterId
from api.activity import getActivityList, signUp, cancelSignUp, getCurrentActivity, checkIn, getSignUpStatistics


class Legym():

    def __init__(self, info):
        data = login(info['username'], info['password'])
        self.headers = {
            'Authorization': 'Bearer '+data['accessToken'],
            'Organization': data['schoolId']
        }
        self.user_id = data['id']
        self.real_name = data['realName']
        print(self.real_name, end=' ')
        self.semester_id = getSemesterId(self.headers)
        print(getSignUpStatistics(self.headers))

    def activityCheckIn(self):
        print('- '+self.real_name)
        for item in getCurrentActivity(self.headers):
            # print(item)
            print('  - '+item['projectName']+' ['+str(item['times'])+']')
            if item['signType'] != 1 and time.time()*1000 < item['timeEnd']:
                r = checkIn(self.headers, self.user_id, item)
                print('    '+r)

    def activitySignUp(self, week, activities, cancel=False):
        print('- '+self.real_name)
        if cancel:
            func = cancelSignUp
        else:
            func = signUp
        self.items = getActivityList(self.headers, week)
        for activity in activities:
            for item in self.items:
                if activity in item['name']:
                    r = func(self.headers, item['id'])
                    print('  - '+activity, r['data']['reason'])
                    break


if __name__ == '__main__':

    weekday = datetime.now().weekday()

    with open('user_info.json', 'r') as f:
        user_info = json.load(f)

    with open('activity_list.json', 'r') as f:
        activity_list = json.load(f)

    if sys.argv[1] == 'checkin':
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

    elif sys.argv[1] == 'signup':
        for k, v in activity_list[str((weekday+2)%7)].items():
            try:
                Legym(user_info[k]).activitySignUp((weekday+2)%7, v)
            except Exception:
                print(k, 'wrong password')
                pass

    elif sys.argv[1] == 'cancelsignup':
        for k, v in activity_list[str((weekday+2)%7)].items():
            try:
                Legym(user_info[k]).activitySignUp((weekday+2)%7, v, True)
            except Exception:
                print(k, 'wrong password')
                pass
