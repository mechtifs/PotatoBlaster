import time
from api.base import login, get_semester_id
from api.activity import get_activity_list, sign_up, cancel_sign_up, get_current_activity_list, check_in, get_sign_up_statistics


class Legym():

    def __init__(self, info):
        data = login(info['username'], info['password'])
        self.headers = {
            'Authorization': 'Bearer '+data['accessToken'],
            'Organization': data['schoolId']
        }
        self.user_id = data['id']
        self.real_name = data['realName']
        self.semester_id = get_semester_id(self.headers)
        stats = get_sign_up_statistics(self.headers)
        print('{} [{}/{}/{}]'.format(self.real_name, stats['signedTimes'], stats['signedTimesNoGrade'], stats['totalTimes']))

    def activity_check_in(self):
        for item in get_current_activity_list(self.headers):
            print('  - '+self.real_name+item['projectName']+' ['+str(item['times'])+']')
            if item['signType'] != 1 and time.time()*1000 < item['timeEnd']:
                r = check_in(self.headers, self.user_id, item)
                print('    '+r)

    def activity_sign_up(self, week, activities, cancel=False):
        if cancel:
            func = cancel_sign_up
        else:
            func = sign_up
        self.items = get_activity_list(self.headers, week)
        for activity in activities:
            for item in self.items:
                if activity in item['name']:
                    r = func(self.headers, item['id'])
                    print('  - '+self.real_name, activity, r['data']['reason'])
                    break
        return r['data']
