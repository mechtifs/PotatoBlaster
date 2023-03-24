from utils import signer, request_till_death


base_url = 'https://cpes.legym.cn'

def get_activity_list(headers, week):
    json = {
        'name': '',
        'campus': '',
        'page': 1,
        'size': 10,
        'state': '',
        'topicId': '',
        'week': week
    }
    r = request_till_death('POST', base_url+'/education/app/activity/getActivityList', headers=headers, json=json)
    json['size'] = r.json()['data']['total']
    r = request_till_death('POST', base_url+'/education/app/activity/getActivityList', headers=headers, json=json)
    return r.json()['data']['items']

def sign_up(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = request_till_death('POST', base_url+'/education/app/activity/signUp', headers=headers, json=json)
    return r.json()

def cancel_sign_up(headers, activityId):
    json = {
        'activityId': activityId
    }
    r = request_till_death('POST', base_url+'/education/app/activity/cancelSignUp', headers=headers, json=json)
    return r.json()

def get_current_activity_list(headers):
    r = request_till_death('GET', base_url+'/education/course/today', headers=headers)
    return r.json()['data']

def check_in(headers, user_id, activity):
    json = {
        'userId': user_id,
        'activityId': activity['courseActivityId'],
        'pageType': 'activity',
        'times': 1,
        'activityType': activity['courseActivityType'],
        'attainabilityType': activity['attainabilityType'],
        'signDigital': signer(activity['courseActivityId']+str(activity['attainabilityType'])+user_id)
    }
    r = request_till_death('PUT', base_url+'/education/activity/app/attainability/sign', headers=headers, json=json)
    return r.json()

def get_sign_up_statistics(headers):
    r = request_till_death('GET', base_url+'/education/app/activity/signUpStatistics', headers=headers)
    return r.json()['data']
