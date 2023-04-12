import aiohttp
import logging
from hashlib import sha1
from logging.handlers import TimedRotatingFileHandler


class Logger:

    def __init__(self, name, path):
        file_path = path+'/'+name+'.log'
        fmt = logging.Formatter('%(asctime)s %(message)s', '%H:%M:%S')
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(TimedRotatingFileHandler(file_path, backupCount=5, when='MIDNIGHT', interval=1))
        self.logger.handlers[0].setFormatter(fmt)
        self.logger.propagate = False

    def log(self, msg):
        self.logger.info(msg)

class TokenExpired(Exception):
    pass

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

async def request_till_death(method, url, **kwargs):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as r:
                    result = await r.json()
                    if r.status == 200 or r.status == 400:
                        return result
                    elif r.status == 401:
                        raise TokenExpired('Token expired when requesting '+url)
                    else:
                        print(r.status)
                        print(kwargs['json'])
                        print(result)
        except Exception as e:
            if isinstance(e, TokenExpired):
                raise e
