import aiohttp
import logging
from hashlib import sha1
from base64 import b64decode
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

def sign(text):
    md = sha1((text+b64decode(b'aXRhdVZmbmV4SGlSaWdaNg==').decode).encode('utf-8')).digest()
    return ''.join(['{:x}{:x}'.format(md[i]>>4&0xf, md[i]&0xf) for i in range(len(md))])

async def request_till_death(method, url, **kwargs):
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as r:
                if r.status < 500:
                    return await r.json()
