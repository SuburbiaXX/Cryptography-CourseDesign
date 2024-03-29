import random
from math import sqrt
from AES import *

"""
if __name__ == '__main__':

    aes = AES()
    key = 0x000102030405060708090a0b0c0d0e0f
    RoundKeys = aes.round_key_generator(key)

    # 加密
    plaintext = 0x00112233445566778899aabbccddeeff
    # 0x00112233445566778899aabbccddeeff -> b'\x00\x11"3DUfw\x88\x99\xaa\xbb\xcc\xdd\xee\xff'
    plaintext = aes.num_2_16bytes(plaintext)
    ciphertext = aes.aes_encrypt(plaintext, RoundKeys)
    print('ciphertext = ' + hex(aes._16bytes2num(ciphertext)))

    # 解密
    ciphertext = 0x69c4e0d86a7b0430d8cdb78070b4c55a
    ciphertext = aes.num_2_16bytes(ciphertext)
    plaintext = aes.aes_decrypt(ciphertext, RoundKeys)
    print('plaintext = ' + hex(aes._16bytes2num(plaintext)))
"""


def EncryptAES(RawStr):
    aes = AES()
    key = random.randint(0x11111111111111111111111111111111, 0xffffffffffffffffffffffffffffffff)
    RoundKeys = aes.round_key_generator(key)

    # 加密
    plaintext = int(RawStr, 16)
    plaintext = aes.num_2_16bytes(plaintext)
    ciphertext = aes.aes_encrypt(plaintext, RoundKeys)
    # print('ciphertext = ' + hex(aes._16bytes2num(ciphertext)))
    return str(hex(aes._16bytes2num(ciphertext)))[2:], key


# def DecryptAES(RawStr):
#
#     ase = AES()
#     # 解密
#     ciphertext = hex(int(RawStr,16))
#     ciphertext = aes.num_2_16bytes(ciphertext)
#     plaintext = aes.aes_decrypt(ciphertext, RoundKeys)
#     print('plaintext = ' + hex(aes._16bytes2num(plaintext)))

# 快速幂
def fast_power(base, power, n):
    result = 1
    tmp = base
    while power > 0:
        if power & 1 == 1:
            result = (result * tmp) % n
        tmp = (tmp * tmp) % n
        power = power >> 1
    return result


# 米勒-罗宾素性检验
# 迭代次数越多可靠性越高
def miller_rabin(n, iter_num=30):
    if n == 2:
        return True
    if n & 1 == 0 or n < 2:
        return False
    m, s = n - 1, 0
    while m & 1 == 0:
        m = m >> 1
        s += 1
    # M-R test
    for _ in range(iter_num):
        b = fast_power(random.randint(2, n - 1), m, n)
        if b == 1 or b == n - 1:
            continue
        for __ in range(s - 1):
            b = fast_power(b, 2, n)
            if b == n - 1:
                break
        else:
            return False
    return True


# 常规确定素性检验方法，不相信就用这个检验一下
def is_prime(n):
    if n > 1:
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for x in range(3, int(sqrt(n) + 1), 2):
            if n % x == 0:
                return False
        return True
    return False


# 随机生成大素数
def generate_prime(PDigits=17, QDigits=17):
    while (1):
        tempstr = ''
        p = tempstr.join(random.choice("123456789"))
        p = p + tempstr.join(random.choice("0123456789") for i in range(PDigits - 1))
        q = tempstr.join(random.choice("123456789"))
        q = q + tempstr.join(random.choice("0123456789") for i in range(QDigits - 1))
        p = int(p)
        q = int(q)
        if p == q:
            continue
        else:
            if miller_rabin(p) and miller_rabin(q):
                return int(p), int(q)


# 扩展欧几里得
def ex_gcd(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1  # 初始化x1,y1,x2,y2
    while b:
        q, r = divmod(a, b)
        a, b = b, r  # gcd(a,b)=gcd(b,a%b)
        # 下面操作模仿矩阵乘法，即
        # [[0,  1]    [[x1, y1]
        #  [1, -q]] x  [x2, y2]]
        x1, y1, x2, y2 = x2, y2, x1 - q * x2, y1 - q * y2
    # 返回一个三元组，依次是(gcd,x,y)，使得 xa+yb=gcd
    return a, x1, y1


# 生成公钥和私钥
def generate_key(phi):
    while (1):
        e = random.randint(2, phi - 1)
        gcd, d, _ = ex_gcd(e, phi)
        if gcd == 1:
            break
    if d < 0:
        d += phi
    return e, d


if __name__ == '__main__':
    p, q = generate_prime(100, 100)
    print("p = ", p)
    print("q = ", q)
    n = p * q
    print("n = ", n)
    phi = (p - 1) * (q - 1)
    e, d = generate_key()
    # print("phi = ", phi)
    print("e = ", e)
    print("d = ", d)

    message = []

    rawmessage = "4a083fcb88204f28ad57f6ebbaf729ec"
    rawmessage = EncryptAES(rawmessage)

    for i in range(0, 4):
        message.append(hex(int(rawmessage[i * 8:8 + i * 8], 16)))
    print(message)

    message = [0x4a083fcb, 0x88204f28, 0xad57f6eb, 0xbaf729ec]

    for i in range(0, 4):
        print("watermark " + str(i) + " :" + str(hex(fast_power(message[i], d, n)))[2:])
