#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
RANDOM_CHAR = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


def random_str(random_length=128):
    sid_str = ''
    chars = RANDOM_CHAR
    length = len(chars) - 1
    for i in range(random_length):
        sid_str += chars[ord(os.urandom(1)) % length]
    return sid_str


def sort_dict(*kwargs):
    i = 0
    for team in kwargs:
       team['id'] = str(i)
       i = i+1
    return kwargs


def check_dict(kwargs):
    try:
        result_dict = json.loads(kwargs)
        return True
    except:
        return None
if __name__ == '__main__':
    pass
