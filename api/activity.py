import requests
from utils import signer


base_url = 'https://cpes.legym.cn'

def getActivityList(headers, week):
    json = {
        'name': '',
        'campus': '',
        'page': 1,
        'size': 10,
        'state': '',
        'topicId': '',
        'week': week
    }
    r = requests.post(base_url+'/education/app/activity/getActivityList', headers=headers, json=json)
    json['size'] = r.json()['data']['total']
    r = requests.post(base_url+'/education/app/activity/getActivityList', headers=headers, json=json)
    return r.json()['data']['items']

def signUp(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = requests.post(base_url+'/education/app/activity/signUp', headers=headers, json=json)
    return r.json()

def cancelSignUp(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = requests.post(base_url+'/education/app/activity/cancelSignUp', headers=headers, json=json)
    return r.json()

def getCurrentActivity(headers):
    r = requests.get(base_url+'/education/course/today', headers=headers)
    return r.json()['data']

def checkIn(headers, user_id, activity):
    json = {
        'userId': user_id,
        'activityId': activity['courseActivityId'],
        'pageType': 'activity',
        'times': 1,
        'activityType': activity['courseActivityType'],
        'attainabilityType': activity['attainabilityType'],
        'signDigital': signer(activity['courseActivityId']+str(activity['attainabilityType'])+user_id)
    }
    r = requests.put(base_url+'/education/activity/app/attainability/sign', headers=headers, json=json)
    return r.json()

def getSignUpStatistics(headers):
    r = requests.get(base_url+'/education/app/activity/signUpStatistics', headers=headers)
    return r.json()['data']