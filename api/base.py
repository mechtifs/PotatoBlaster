import requests


base_url = 'https://cpes.legym.cn'

def login(username, password):
    json = {
        'entrance': '1',
        'userName': username,
        'password': password
    }
    r = requests.post(base_url+'/authorization/user/manage/login', json=json)
    return r.json()['data']


def getSemesterId(headers):
    r = requests.get(base_url+'/education/semester/getCurrent', headers=headers)
    return r.json()['data']['id']
