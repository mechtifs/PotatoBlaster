from base64 import b64decode
from utils import sign, request_till_death


base_url = b64decode('aHR0cHM6Ly9jcGVzLmxlZ3ltLmNu').decode()

async def get_activity_list(headers, week):
    json = {
        'name': '',
        'campus': '',
        'page': 1,
        'size': 10,
        'state': '',
        'topicId': '',
        'week': week
    }
    r = await request_till_death('POST', base_url+'/education'+'/app'+'/activity'+'/getActivityList', headers=headers, json=json)
    json['size'] = r['data']['total']
    r = await request_till_death('POST', base_url+'/education'+'/app'+'/activity'+'/getActivityList', headers=headers, json=json)
    return r['data']['items']

async def signup(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = await request_till_death('POST', base_url+'/education'+'/app'+'/activity'+'/signUp', headers=headers, json=json)
    return r

async def cancel_signup(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = await request_till_death('POST', base_url+'/education'+'/app'+'/activity'+'/cancelSignUp', headers=headers, json=json)
    return r

async def get_current_activity_list(headers):
    r = await request_till_death('GET', base_url+'/education'+'/course'+'/today', headers=headers)
    return r['data']

async def checkin(headers, user_id, activity):
    json = {
        'userId': user_id,
        'activityId': activity['courseActivityId'],
        'pageType': 'activity',
        'times': 1,
        'activityType': activity['courseActivityType'],
        'attainabilityType': activity['attainabilityType'],
        'signDigital': sign(activity['courseActivityId']+str(activity['attainabilityType'])+user_id)
    }
    r = await request_till_death('PUT', base_url+'/education'+'/activity'+'/app'+'/attainability'+'/sign', headers=headers, json=json)
    return r

async def get_signup_statistics(headers):
    r = await request_till_death('GET', base_url+'/education'+'/app'+'/activity'+'/signUpStatistics', headers=headers)
    return r['data']
