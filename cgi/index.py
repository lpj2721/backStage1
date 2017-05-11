#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, redirect
import json
import conf
from db_conn.cont_redis import g_session_redis
from login import Login
from Interface import Interfaces
from headerConfig import HeaderConfig

app = Flask(__name__)
app.debug = conf.debug_mode


def pre_do(c, fun, ext_type=None):
    req_dict = {}
    sid = request.headers.get('access-token')
    if ext_type is not "login":
        if sid == '':
            out = {"message": "会话超时！"}
            resp = make_response(json.dumps(out), 401)
            return resp
    if request.method == "POST":
        if ext_type=="file_up":
            req_dict["input"] = {"opr": "upload"}
        elif ext_type=="ext_type":
            req_dict["input"] = dict(opr="update", data=request.get_data())
            pass
        else:
            try:
                req_dict["input"] = json.loads(request.get_data())
            except:
                return conf.err["refused"]
    elif request.method == "PATCH":
        req_dict["input"] = json.loads(request.get_data())
        return json.dumps(req_dict)
    ip = request.headers.get('X-Real-IP')
    if ip is None or ip == "":
        ip = "127.0.0.1"
    req_dict["self"] = {}
    req_dict["self"]["ip"] = ip
    req_dict["self"]["token"] = sid
    req_dict["self"]["m"] = request.method
    req_dict["self"]["fun"] = fun

    c.setenv(req_dict)
    try:
        c.myinit()
        c.setenv(req_dict)
        c.onInit()
    except:
        c.mydel()
        raise
    out = c.output()
    redirect_url = c.redirect_url
    c.mydel()

    if redirect_url is not None:
        return redirect(redirect_url)
    token = g_session_redis.get('token')
    resp = make_response(out)
    resp.headers['access-token'] = token
    resp.headers['x-total-count'] = 6
    return resp


@app.route(conf.url_pre + "login", methods = ['GET', 'POST', 'PATCH'])
def login_func():
    return pre_do(Login(), "login", ext_type="login")


@app.route(conf.url_pre + "interface", methods = ['GET', 'POST', 'PATCH'])
def interface_func():
    return pre_do(Interfaces(), "Interfaces")


@app.route(conf.url_pre + "headerConfig", methods = ['GET', 'POST', 'PATCH'])
def header_config_func():
    return pre_do(HeaderConfig(), "headerConfig")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
