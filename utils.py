from hashlib import sha1


hex_digits = '0123456789abcdef'
salt = 'itauVfnexHiRigZ6'


def signer(str):
    str += salt
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
