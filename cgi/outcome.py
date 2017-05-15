#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/15 9:18
"""
import json
from lib_util import check_dict
from wx_cgibase import cgibase
from wx_opr.basic_info import BasicInfo


class Interfaces(cgibase):
    def __init__(self):
        self.oprList = {
            "fetch": self.fetch,
            "search": self.search,
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
            result, total = BasicInfo().fetch_interface(page=page, page_size=page_size)
            res = {"success": True, "data": result, 'total': total}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out

    def search(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("search in.")
        data = self.input["input"]["data"]
        if data:
            BasicInfo().create_interface(**data)
            res = {"success": True, "message": "Ok！"}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out


if __name__ == "__main__":
    pass