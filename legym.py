import asyncio
from api.base import login, get_semester_id
from api.activity import get_activity_list, signup, cancel_signup, get_current_activity_list, checkin, get_signup_statistics


class Legym():

    def __init__(self, info):
        self.username = info['username']
        self.password = info['password']
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()

    async def login(self):
        data = await login(self.username, self.password)
        self.headers = {
            'Authorization': 'Bearer '+data['accessToken'],
            'Organization': data['schoolId']
        }
        self.user_id = data['id']
        self.real_name = data['realName']
        self.semester_id = await get_semester_id(self.headers)
        stats = await get_signup_statistics(self.headers)
        print('{} [{}/{}/{}]'.format(self.real_name, stats['signedTimes'], stats['signedTimesNoGrade'], stats['totalTimes']))

    async def checkin_coro(self, item):
        print('  - {}\t{} [{}]'.format(self.real_name, item['projectName'], item['times']))
        if item['signType'] != 1:
            r = await checkin(self.headers, self.user_id, item)
            print('    '+str(r))
            r['activity'] = item['projectName']
            return r

    async def signup_coro(self, activity, func, items):
        for item in items:
            if activity in item['name']:
                r = await func(self.headers, item['id'])
                print('  - '+self.real_name, activity, r['data']['reason'])
                r['activity'] = item['name']
                return r

    def activity_checkin(self):
        self.loop.run_until_complete(self.login())
        items = self.loop.run_until_complete(get_current_activity_list(self.headers))
        tasks = [self.loop.create_task(self.checkin_coro(item)) for item in items]
        result = self.loop.run_until_complete(asyncio.wait(tasks))
        return [r.result() for r in result[0]]

    def activity_signup(self, week, activities, cancel=False):
        self.loop.run_until_complete(self.login())
        func = cancel_signup if cancel else signup
        items = self.loop.run_until_complete(get_activity_list(self.headers, week))
        tasks = [self.loop.create_task(self.signup_coro(activity, func, items)) for activity in activities]
        result = self.loop.run_until_complete(asyncio.wait(tasks))
        return [r.result() for r in result[0]]
