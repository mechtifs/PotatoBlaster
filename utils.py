import requests
from hashlib import sha1


def signer(str):
    hex_digits = '0123456789abcdef'
    str += 'itauVfnexHiRigZ6'
    md = sha1(str.encode('utf-8')).digest()
    j = len(md)
    buf = [0]*(j*2)
    k = 0
    for i in range(j):
        byte0 = md[i]
        buf[k] = hex_digits[byte0>>4&0xf]
        k += 1
        buf[k] = hex_digits[byte0&0xf]
        k += 1
    return ''.join(buf)

def request_till_death(method, url, params=None, data=None, json=None, headers=None):
    while True:
        try:
            if method == 'GET':
                r = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                r = requests.post(url, data=data, json=json, headers=headers)
            elif method == 'PUT':
                r = requests.put(url, data=data, json=json, headers=headers)
            elif method == 'DELETE':
                r = requests.delete(url, params=params, headers=headers)
            break
        except requests.exceptions.RequestException:
            pass
    return r
