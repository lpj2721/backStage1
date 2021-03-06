#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
from lib_util import check_dict
from wx_cgibase import cgibase
from wx_opr.basic_info import BasicInfo


class Interfaces(cgibase):
    def __init__(self):
        self.oprList = {
            "fetch": self.fetch,
            "create": self.create,
            "modify": self.modify,
            "remove": self.remove,
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

    def create(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("join in.")
        data = self.input["input"]["data"]
        if data:
            BasicInfo().create_interface(**data)
            res = {"success": True, "message": "Ok！"}
            self.out = json.dumps(res)
        else:
            res = {"success":False,"message":"Ok！"}
            self.out = json.dumps(res)
        return self.out

    def modify(self):

        '''{"opr":"login","data":{"username":"admin","password":"123456"}}'''
        self.log.debug("modify in.")
        data = self.input["input"]["data"].get('data')
        parameter = data.get('request_parameter')
        headers = data.get('Interface_header')
        for check_parameter in [parameter, headers]:
            if check_dict(check_parameter) is None:
                res = {"success": False, "message": "输入有误！"}
                self.out = json.dumps(res)
                return self.out
        if data:
            result = BasicInfo().modify_interface(**data)
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

    def remove(self):
        self.log.debug("remove in.")
        data = self.input['input']['data'].get('id')
        if data:
            BasicInfo().remove_interface(data)
            res = {"success": True, "message": "Ok！"}
            self.out = json.dumps(res)
        else:
            res = {"success": False, "message": "输入有误！"}
            self.out = json.dumps(res)
        return self.out


if __name__ == "__main__":
    pass
