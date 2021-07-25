# -*- coding: utf-8 -*-
"""
Created on Fri May 21 22:09:07 2021

@author: 孔令百
"""

import jwt
import time
import random
import string
import yagmail

key='1852146konglingbai'                            #密钥
token_period=10800                                  #时效3小时
def generate_jwt(uid):
    payload = {
        'iss':'https://github.com/lingbai-kong',    # iss 【issuer】发布者的url地址
        'exp': time.time()+token_period,            # exp 【expiration】 该jwt销毁的时间；unix时间戳
        'iat': time.time(),                         # iat 【issued at】 该jwt的发布时间；unix 时间戳
        'uid': uid
    }
    # headers
    headers = {
        'alg': "HS256",  # 声明所使用的算法
    }

    jwt_token = jwt.encode(
        payload,                                    # payload, 有效载体 
        key,                                        # 进行加密签名的密钥
        algorithm='HS256',                          # 指明签名算法方式, 默认也是HS256
        headers=headers                             # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
        ).decode('ascii')                           # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
    return jwt_token
def check_jwt(JWT):
    data={}
    try:
        data = jwt.decode(JWT,key,algorithms=['HS256'])
    # 如果 jwt 被篡改过; 或者算法不正确; 如果设置有效时间, 过了有效期; 或者密钥不相同; 都会抛出相应的异常
    except Exception as e:
        return e
    return data['uid']

def generate_uid():
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(10)]
    random_str = ''.join(str_list)
    return random_str
def generate_auth():
    str_list = [random.choice(string.digits) for i in range(6)]
    random_str = ''.join(str_list)
    return random_str
def auth_send(auth,email):
    yag=yagmail.SMTP(user='tjdbstock@163.com',password='TXKVYVTSRRZCBNRM',host='smtp.163.com')
    body=f'【股票交易系统】您好，您的验证码为:{auth}\n如果不是本人操作，请忽略。'
    yag.send(to=email,subject='股票交易系统账户邮箱验证码',contents=[body])
if __name__ == '__main__':
    uid='123123'
    JWT=generate_jwt(uid)
    print(JWT)
    token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2dpdGh1Yi5jb20vbGluZ2JhaS1rb25nIiwiZXhwIjoxNjIxNjIzMzM0Ljg3Nzc5ODgsImlhdCI6MTYyMTYxMjUzNC44Nzc3OTg4LCJ1aWQiOiJIdW5kcmVkS0wifQ.zXb1XA0DZG661qjJ31p7v1VkQ-6Y90W3FoAqaIuIbTw'
    uid=check_jwt(token)
    print(uid)
    print(generate_uid())