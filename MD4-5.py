import sys
import os
import math
# 162020228陈泰伦 -> 前9位是数字，后三位是汉字
# b'162020228\xe9\x99\x88\xe6\xb3\xb0\xe4\xbc\xa6' 需要448位，填充10000...
# 一个汉字转三字节，也就是24位，两到四个汉字就是六到十二字节，也就是48~96位，加上数字位的int类型8位，总共是56~104位
from Crypto.Hash import MD4
from Crypto.Hash import MD5

def HexadecimalToBinary(str):
    """
    负责将表达单个十六进制数字的字符转化为对应二进制的字符
    :param str:
    :return:
    """
    ReturnStr = ""
    if (str >= '0') & (str <= '9'):
        if str == '0':
            ReturnStr = '0000'
        if str == '1':
            ReturnStr = '0001'
        if str == '2':
            ReturnStr = '0010'
        if str == '3':
            ReturnStr = '0011'
        if str == '4':
            ReturnStr = '0100'
        if str == '5':
            ReturnStr = '0101'
        if str == '6':
            ReturnStr = '0110'
        if str == '7':
            ReturnStr = '0111'
        if str == '8':
            ReturnStr = '1000'
        if str == '9':
            ReturnStr = '1001'
    else :
        if str == "a":
            ReturnStr = '1010'
        if str == "b":
            ReturnStr = '1011'
        if str == "c":
            ReturnStr = '1100'
        if str == "d":
            ReturnStr = '1101'
        if str == "e":
            ReturnStr = '1110'
        if str == "f":
            ReturnStr = '1111'
    return ReturnStr

def TotalTransferHexToBin(str):
    """
    负责将一连串的十六进制字符串转化为二进制字符串
    :param str:
    :return:
    """
    ReturnStr = ""
    for i in str:
        ReturnStr = ReturnStr + HexadecimalToBinary(i)
    return ReturnStr

def TotalTransferDecimalToBin(str):
    """
    负责将一连串的十进制字符串转化为二进制字符串
    :param str:
    :return:
    """
    str = int(str)
    ReturnStr = bin(str)
    ReturnStr = ReturnStr[2:]
    return ReturnStr

def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class MD5(object):
    # 初始化密文
    def __init__(self, message):
        self.message = message
        self.ciphertext = ""

        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.init_A = 0x67452301
        self.init_B = 0xEFCDAB89
        self.init_C = 0x98BADCFE
        self.init_D = 0x10325476
        '''
        self.A = 0x01234567
        self.B = 0x89ABCDEF
        self.C = 0xFEDCBA98
        self.D = 0x76543210
         '''

        self.T = [0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
                    0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
                    0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
                    0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
                    0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
                    0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
                    0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
                    0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]
        self.s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
                    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
                    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
                    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
        self.m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                    1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12,
                    5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2,
                    0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]

    # 附加填充位
    def fill_text(self):
        for i in range(len(self.message)):
            c = int2bin(ord(self.message[i]), 8)
            self.ciphertext += c

        if (len(self.ciphertext)%512 != 448):
            if ((len(self.ciphertext)+1)%512 != 448):
                self.ciphertext += '1'
            while (len(self.ciphertext)%512 != 448):
                self.ciphertext += '0'

        length = len(self.message)*8
        if (length <= 255):
            length = int2bin(length, 8)
        else:
            length = int2bin(length, 16)
            temp = length[8:12]+length[12:16]+length[0:4]+length[4:8]
            length = temp

        self.ciphertext += length
        while (len(self.ciphertext)%512 != 0):
            self.ciphertext += '0'

    # 分组处理（迭代压缩）
    def circuit_shift(self, x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def change_pos(self):
        a = self.A
        b = self.B
        c = self.C
        d = self.D
        self.A = d
        self.B = a
        self.C = b
        self.D = c

    def FF(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.F(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def GG(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.G(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def HH(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.H(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def II(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.I(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()


    def F(self, X, Y, Z):
        return (X & Y) | ((~X) & Z)
    def G(self, X, Y, Z):
        return (X & Z) | (Y & (~Z))
    def H(self, X, Y, Z):
        return X ^ Y ^ Z
    def I(self, X, Y, Z):
        return Y ^ (X | (~Z))

    def group_processing(self):
        M = []
        for i in range(0, 512, 32):
            num = ""
            # 获取每一段的标准十六进制形式
            for j in range(0, len(self.ciphertext[i:i+32]), 4):
                temp = self.ciphertext[i:i+32][j:j + 4]
                temp = hex(int(temp, 2))
                num += temp[2]
            # 对十六进制进行小端排序
            num_tmp = ""
            for j in range(8, 0, -2):
                temp = num[j-2:j]
                num_tmp += temp

            num = ""
            for i in range(len(num_tmp)):
                num += int2bin(int(num_tmp[i], 16), 4)
            M.append(num)

        #print(M)



        for j in range(0, 16, 4):
            self.FF(M[self.m[j]], self.s[j], self.T[j])
            self.FF(M[self.m[j+1]], self.s[j+1], self.T[j+1])
            self.FF(M[self.m[j+2]], self.s[j+2], self.T[j+2])
            self.FF(M[self.m[j+3]], self.s[j+3], self.T[j+3])

        for j in range(0, 16, 4):
            self.GG(M[self.m[16+j]], self.s[16+j], self.T[16+j])
            self.GG(M[self.m[16+j+1]], self.s[16+j+1], self.T[16+j+1])
            self.GG(M[self.m[16+j+2]], self.s[16+j+2], self.T[16+j+2])
            self.GG(M[self.m[16+j+3]], self.s[16+j+3], self.T[16+j+3])


        for j in range(0, 16, 4):
            self.HH(M[self.m[32+j]], self.s[32+j], self.T[32+j])
            self.HH(M[self.m[32+j+1]], self.s[32+j+1], self.T[32+j+1])
            self.HH(M[self.m[32+j+2]], self.s[32+j+2], self.T[32+j+2])
            self.HH(M[self.m[32+j+3]], self.s[32+j+3], self.T[32+j+3])


        for j in range(0, 16, 4):
            self.II(M[self.m[48+j]], self.s[48+j], self.T[48+j])
            self.II(M[self.m[48+j+1]], self.s[48+j+1], self.T[48+j+1])
            self.II(M[self.m[48+j+2]], self.s[48+j+2], self.T[48+j+2])
            self.II(M[self.m[48+j+3]], self.s[48+j+3], self.T[48+j+3])

        self.A = (self.A+self.init_A)%pow(2, 32)
        self.B = (self.B+self.init_B)%pow(2, 32)
        self.C = (self.C+self.init_C)%pow(2, 32)
        self.D = (self.D+self.init_D)%pow(2, 32)

        answer = ""
        for register in [self.A, self.B, self.C, self.D]:
            register = hex(register)[2:]
            for i in range(8, 0, -2):
                answer += str(register[i-2:i])

        return answer

def GetRawInfo(path):
    """
    从utf-8编码的，在path路径的文本文件里获取学号+姓名，并转化为基本的二进制形式
    :param path:
    :return:
    """
    file = open(path, encoding='utf-8')

    RawStr = ""
    for i in file:
        RawStr = RawStr + i
    RawStr = RawStr.encode("utf-8")
    file.close()
    RawStr = str(RawStr)

    StrLen = len(RawStr)
    StudentNumber = RawStr[2:11]
    StudentName = ""
    for i in range(13, StrLen):
        if (i + 1) // 2 % 2 != 0:
            StudentName = StudentName + RawStr[i]

    StudentNumber = TotalTransferDecimalToBin(StudentNumber)
    StudentName = TotalTransferHexToBin(StudentName)
    RawMD5 = StudentNumber + StudentName
    return RawMD5

MD5 = MD5(GetRawInfo("before.txt"))
MD5.fill_text()
result = MD5.group_processing()

print("MD5加密：{}".format(result))