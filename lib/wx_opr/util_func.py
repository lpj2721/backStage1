#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/15 14:58
"""
import copy
import json
from lib_post import post
from db_conn.cont_mongo import MongoConn
from wx_opr.basic_info import BasicInfo


def post_work(serial_num):
    test_cache = BasicInfo().search_outcome(serial_num)
    for each in test_cache:
        header = each['Interface_header']
        body = json.dumps(each['request_parameter'])
        url = each['Interface_address']
        resp_status, resp_body = post(url=url, datas=body, headers=header)
        each['status-code'] = resp_status
        each['response'] = resp_body
        MongoConn().db['data_source'].update_one({'_id': each['_id']}, {"$set": each})
    return True