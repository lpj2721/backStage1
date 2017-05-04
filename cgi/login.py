#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
from conf import *
import json
from lib_util import randomStr
from db_conn.cont_redis import g_session_redis
from wx_cgibase import cgibase
from wx_opr.basic_info import BasicInfo


class Login(cgibase):
    def __init__(self):
        self.oprList = {
            "login": self.login
        }
        return cgibase.__init__(self)

    def onInit(self):
        cgibase.SetNoCheckCookie(self)
        opr = cgibase.onInit(self)
        if opr is None:
            return
        if opr not in self.oprList :
            return
        self.oprList[opr]()

    def login(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("join in.")
        data = self.input["input"]["data"]
        user_name = data['username']
        result = BasicInfo().userLogin(username=data['username'], password=data['password'])
        if result:
            self.token = randomStr()
            g_session_redis.set(g_redis_pix + self.token, user_name)
            g_session_redis.set(user_name, g_redis_pix + self.token)
            g_session_redis.set('token',g_redis_pix + self.token)
            g_session_redis.expire(g_redis_pix + self.token, g_ssid_timeout)
            res = {"success": True, "message": "Ok！"}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out

if __name__ == "__main__":
    login = Login()
    login.onInit()
