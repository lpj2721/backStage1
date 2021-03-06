#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/11 16:15
"""

import json
from lib_util import check_dict
from wx_cgibase import cgibase
from wx_opr.basic_info import BasicInfo


class HeaderConfig(cgibase):
    def __init__(self):
        self.oprList = {
            "fetch": self.fetch,
            "modify": self.modify,
            "post": self.post,
        }
        return cgibase.__init__(self)

    def onInit(self):
        # cgibase.SetNoCheckCookie(self)
        opr = cgibase.onInit(self)
        if opr is None:
            return
        if opr not in self.oprList :
            return
        self.oprList[opr]()

    def fetch(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("fetch in.")
        data = self.input["input"]["data"]
        page = int(data['page'])
        page_size = data['PAGE_SIZE']
        if data:
            result, total = BasicInfo().fatch_rules(page=page, page_size=page_size)
            res = {"success": True, "data": result, 'total': total}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out

    def modify(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("modify in.")
        data = self.input["input"]["data"].get('data')
        if data:
            result = BasicInfo().modify_rules(**data)
            if result:
                res = {"success": True, "message": "Ok！"}
                self.out = json.dumps(res)
            else:
                res = {"success":False,"message":"更新失败！"}
                self.out = json.dumps(res)
        else:
            res = {"success": False, "message": "输入有误！"}
            self.out = json.dumps(res)
        return self.out

    def post(self):
        self.log.debug("post in.")
        data = self.input["input"]["data"].get('id')
        if data:
            result = BasicInfo().interface_post(data)
            res = {"success": True, "data": result}
            self.out = json.dumps(res)
        return self.out

if __name__ == "__main__":
    pass