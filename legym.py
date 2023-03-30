from api.base import login, get_semester_id
from api.activity import get_activity_list, signup, cancel_signup, get_current_activity_list, checkin, get_signup_statistics


class Legym():

    def __init__(self, info):
        self.username = info['username']
        self.password = info['password']

    async def login(self):
        data = await login(self.username, self.password)
        if not data:
            return None
        self.headers = {
            'Authorization': 'Bearer '+data['accessToken'],
            'Organization': data['schoolId']
        }
        self.user_id = data['id']
        self.real_name = data['realName']
        self.semester_id = await get_semester_id(self.headers)
        stats = await get_signup_statistics(self.headers)
        print('{} [{}/{}/{}]'.format(self.real_name, stats['signedTimes'], stats['signedTimesNoGrade'], stats['totalTimes']))
        return self.user_id

    async def activity_checkin(self):
        res = []
        items = await get_current_activity_list(self.headers)
        for item in items:
            print('  - {}\t{} [{}]'.format(self.real_name, item['projectName'], item['times']))
            if item['signType'] != 1:
                r = await checkin(self.headers, self.user_id, item)
                print('    '+str(r))
                r['activity'] = item['projectName']
                res.append(r)
        return res

    async def activity_signup(self, week, activities, cancel=False):
        func = cancel_signup if cancel else signup
        res = []
        items = await get_activity_list(self.headers, week)
        for activity in activities:
            for item in items:
                if activity in item['name']:
                    r = await func(self.headers, item['id'])
                    print('  - '+self.real_name, activity, r['data']['reason'])
                    r['activity'] = item['name']
                    res.append(r)
        return res
