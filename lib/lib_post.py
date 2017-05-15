#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/15 10:28
"""
import requests


def post(url, **headers, **data):
    default_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.96 Safari/537.36"
    }
    s = requests.Session()
    s.headers.update(default_header)
    response = s.post(url=url, headers=headers, data=data, verify=False)
    status_code = response.status_code
    body = response.text
    return status_code, body


def get(url, **headers, **data):
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
