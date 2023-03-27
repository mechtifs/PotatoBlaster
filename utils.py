import os
import logging
import requests
from hashlib import sha1
from logging.handlers import RotatingFileHandler


class Logger:

    def __init__(self, name, path):
        file_path = path+'/'+name+'.log'
        fmt = logging.Formatter('%(asctime)s\t%(message)s', '%H:%M:%S')
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(RotatingFileHandler(file_path, maxBytes=1024*1024*10, backupCount=5))
        self.logger.handlers[0].setFormatter(fmt)
        self.logger.propagate = False

    def log(self, msg):
        self.logger.info(msg)

def sign(str: str):
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
            if r.status_code < 500:
                return r
        except requests.exceptions.RequestException:
            pass
