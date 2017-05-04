#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
from conf import *
import json
from lib_util import randomStr
from db_conn.cont_redis import g_session_redis
from wx_cgibase import cgibase
from wx_opr.basic_info import BasicInfo


class Users(cgibase):
    def __init__(self):
        self.oprList = {
            "create": self.create,
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

    def create(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("join in.")
        data = self.input["input"]["data"]
        print(data)
        if data:
            res = {"success": True, "message": "Ok！"}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out


if __name__ == "__main__":
    pass
