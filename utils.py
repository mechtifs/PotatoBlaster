import aiohttp
import logging
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

async def sign(str):
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

async def request_till_death(method, url, params=None, data=None, json=None, headers=None):
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                if method == 'GET':
                    r = await session.get(url, params=params, headers=headers)
                elif method == 'POST':
                    r = await session.post(url, data=data, json=json, headers=headers)
                elif method == 'PUT':
                    r = await session.put(url, data=data, json=json, headers=headers)
                if r.status < 500:
                    return await r.json()
            except (aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError, aiohttp.ServerFingerprintMismatch, aiohttp.ServerTimeoutError):
                pass
