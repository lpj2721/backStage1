#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/15 10:28
"""
import json
import requests


def post(url, datas, **headers):
    default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.96 Safari/537.36"
    }
    if headers:
        response = requests.post(url=url, headers=headers, data=datas, verify=False)
    else:
        response = requests.post(url=url,headers=default_header, data=json.dumps(datas),verify=False)

    status_code = response.status_code
    print(status_code)
    body = response.text
    return status_code, body


def get(url, data, **headers):
    default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.96 Safari/537.36"
    }
    s = requests.Session()
    s.headers.update(default_header)
    response = s.get(url=url, headers=headers, data=data, verify=False)
    status_code = response.status_code
    body = response.text
    return status_code, body

if __name__ == '__main__':
    pass
    # data = {"opr":"login","data":{"username":"admin","password":"123456"}}
    # url = 'http://127.0.0.1:5000/login'
    # a, b = post(url, data)
    # print(a,b)