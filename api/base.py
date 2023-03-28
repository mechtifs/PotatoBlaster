from utils import request_till_death


base_url = 'https://cpes.legym.cn'

async def login(username, password):
    json = {
        'entrance': '1',
        'userName': username,
        'password': password
    }
    r = await request_till_death('POST', base_url+'/authorization/user/manage/login', json=json)
    return r['data']

async def get_semester_id(headers):
    r = await request_till_death('GET', base_url+'/education/semester/getCurrent', headers=headers)
    return r['data']['id']
