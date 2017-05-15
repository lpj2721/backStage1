#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/5/15 14:58
"""
import copy

def rules_analysis(*args):
    rules_name = []
    rules_arg = {}
    for each in args:
        rules_name.append(each['arg_name'])
        rules_arg[each['arg_name']] = each['arg_rules']
    return rules_name, rules_arg


def list_combination(args=(0,)):
    lengths = []  # 数据各个子数组的长度
    totalLength = 1
    for row in args:
        length = len(row)
        lengths.append(length)
        totalLength *= length
        pass
    result = (0,)
    for i in range(totalLength):
        j = 0
        for len in lengths:
            result = result + (args[j][i % len],)
            i = int(i / len)
            j += 1
            pass
        pass
    return result