# -*- coding: utf-8 -*-
from db_conn.cont_mongo import MongoConn
from db_conn.cont_redis import g_session_redis
import time
import traceback
import random
import json
import copy


class BasicInfo:
    def __init__(self):
        self.db = MongoConn().db

    def user_login(self, username,password):
        user_info = self.db['user_open'].find_one({'_id': username})
        if user_info and user_info['password']==password:
            return True
        else:
            return False

    def create_interface(self, **kwargs):
        arg_rules = {
            '_id': kwargs['_id'],
            'parameter_rules': '',
            'header_rules': ''
        }
        try:
            self.db['template_rules'].insert_one(arg_rules)
            self.db['interface_template'].insert_one(kwargs)
            return True
        except Exception:
            return traceback.format_exc()
    @staticmethod
    def rules_analysis(*args):
        rules_name = []
        rules_arg = {}
        for each in args:
            print(each)
            rules_name.append(each['arg_name'])
            rules_arg[each['arg_name']] = each['arg_rules']
        return rules_name, rules_arg

    def fatch_rules(self,page, page_size):
        pages = (page - 1) * page_size
        total = self.db['template_rules'].find({}).count()
        templates = self.db['template_rules'].find({}).skip(pages).limit(page_size)
        result = []
        for template in templates:
            result.append(template)
        return result, total

    def fetch_interface(self,page, page_size):
        pages = (page - 1) * page_size
        total = self.db['interface_template'].find({}).count()
        templates = self.db['interface_template'].find({}).skip(pages).limit(page_size)
        result = []
        for template in templates:
            result.append(template)
        return result, total

    def fetch_outcome(self,page, page_size):
        pages = (page - 1) * page_size
        total = self.db['data_source'].find({}).count()
        templates = self.db['data_source'].find({},{'_id': 0}).skip(pages).limit(page_size)
        result = []
        for template in templates:
            template['request_parameter'] = json.dumps(template['request_parameter'])
            if template['response'] == '':
                template['response'] = "测试正在进行，请耐心等待结果"
            result.append(template)
        return result, total

    def search_outcome(self,serial_num):
        templates = self.db['data_source'].find({'serial_num': serial_num})
        result = []
        for template in templates:
            result.append(template)
        return result

    def modify_interface(self,**kwargs):
        _id = kwargs.get('_id')
        del kwargs['_id']
        print(kwargs)
        if _id:
            self.db['interface_template'].update_one({'_id': _id},{"$set": kwargs})
            return True
        else:
            return False

    def modify_rules(self,**kwargs):
        _id = kwargs.get('_id')
        del kwargs['_id']
        if _id:
            self.db['template_rules'].update_one({'_id': _id},{"$set": kwargs})
            return True
        else:
            return False

    def remove_interface(self,_id):
        self.db['interface_template'].delete_one({'_id':_id})

    def interface_post(self, _id):
        interface_template = self.db['interface_template'].find_one(_id)
        request_parameter = json.loads(interface_template['request_parameter'])
        serial_num = ("%.6f" % time.time()).replace(".", "") + str(random.randint(100, 999))
        template_rules = self.db['template_rules'].find_one(_id)
        rules = eval(template_rules['parameter_rules'])
        rules_name, rules_arg = self.rules_analysis(*rules)
        copy_parameter = copy.deepcopy(request_parameter)
        if rules_name == list(request_parameter.keys()):
            data = ()
            for each in rules_arg.values():
                a = tuple(each)
                data += (a,)
            lengths = []  # 数据各个子数组的长度
            totalLength = 1
            for row in data:
                length = len(row)
                lengths.append(length)
                totalLength *= length
                pass
            for i in range(totalLength):
                j = 0
                result = ()
                for lens in lengths:
                    result += (data[j][i % lens],)
                    i = int(i / lens)
                    j += 1
                    pass
                k = 0
                for name in rules_name:
                    copy_parameter[name] = result[k]
                    k += 1
                data_source = {
                    "serial_num": serial_num,
                    "test_name": _id,
                    "Interface_address": interface_template['Interface_address'],
                    "Interface_header": interface_template['Interface_header'],
                    "request_parameter": copy_parameter,
                    "response": "",
                    "status-code": 0
                }
                self.db['data_source'].insert_one(data_source)
            g_session_redis.lpush('test_queue',serial_num)
            return serial_num

    def get_dishInfo(self, store_id):
        dishInfo = self.db['business_info'].find_one(store_id, {'_id': 0, 'dishes': 1, 'dish': 1})
        dish_type = sorted(dishInfo['dishes'], key=lambda type_sn: type_sn['type_sn'])
        #菜品
        dish_cont = dishInfo['dish']
        result = []
        food = {}
        str_dix = "cate"
        if dish_type:
            for item in dish_type:
                #分类
                food['cate_id'] = str_dix + item['id']
                food['cate_name'] = item['type_name']
                food['cate_mark'] = item['type_remark']
                dish_dix = "dish" + item['id'] + "-"
                sn = 0
                dishs = []
                if len(dish_cont) == 0:
                    food['dishs'] = dishs
                else:
                    #菜品筛选
                    for each in dish_cont:
                        dish = {}
                        if item['type_name'] == each['type_name']:
                            #下架菜品不返回给前端
                            if each['dish_num'] ==1:
                                break
                            dish['dish_id'] = dish_dix + str(sn)
                            dish['dish_name'] = each['dish_name']
                            dish['dish_price'] = each['price']
                            dish['discount'] = each['discount']
                            dish['dish_count'] = 0
                            dish['dish_pic'] = each['image_url']
                            dish['dish_sale'] = each['sales']
                            copy_d = copy.deepcopy(dish)
                            dishs.append(copy_d)
                            sn = sn + 1
                        else:
                            pass
                    food['dishs'] = copy.deepcopy(dishs)
                copy_f = copy.deepcopy(food)
                result.append(copy_f)
            for j in range(len(result) - 1, -1, -1):
                if len(result[j]['dishs']) == 0:
                    result.pop(j)
            return result
        else:
            return result

    def get_storeInfo(self, store_id):
        storeInfo = self.db['business_info'].find_one(store_id, {'_id': 0, 'b_name':1,'b_notice': 1})
        return storeInfo

    def sub_order(self, **kwargs):
        serial_num = kwargs['_id']
        store_id = kwargs['business_id']
        user_id = kwargs['consumer_id']
        dish_name = kwargs['dishs'][0]['dish_name']
        dish_count = kwargs['count']
        create_time = kwargs['create_time']
        status = kwargs['status']
        money = kwargs['money']
        pay_for = kwargs['pay_for']
        desk_id = kwargs['desk_id']
        timestamp = time.time() * 1000
        create_times = create_time[:10]
        local_str_time = create_times.replace("-", "")
        order_list = self.db['consumer_info'].find_one(user_id, {'_id': 0, 'order_list': 1})
        order_list['order_list'].insert(0, serial_num)
        self.db['consumer_info'].update_one({"_id": user_id}, {"$set": {'order_list': order_list['order_list']}})
        order_info = {
            'id': timestamp,
            'serial_num': serial_num,
            'status': status,
            'dish_name': dish_name,
            'dish_count': dish_count,
            'desk_id': desk_id,
            'money': money,
            'create_time': create_time,
            'pay_for': pay_for
        }
        if self.db[store_id].find_one(local_str_time):
            # 商户订单表更新
            self.db[store_id].update_one({"_id": local_str_time}, {"$push": {'order_list': order_info}})
            self.db[store_id].update_one({"_id": local_str_time}, {"$inc": {'order_total': 1}})
        else:
            order_list = []
            order_list.append(order_info)
            day_orders = {
                '_id': local_str_time,
                'money_total': 0,
                'order_total': 1,
                'order_list': order_list
            }
            self.db[store_id].insert_one(day_orders)
        result = self.db['order_info'].insert_one(kwargs)
        if result.inserted_id:
            return True
        else:
            return False

    def modify_order(self, pay_serial_num=None,store_id=None, serial_num=None, status=None):
        order_info  = self.db['order_info'].find_one(serial_num,{"_id":0,"create_time":1})
        create_time = order_info['create_time'][:10]
        local_str_time = create_time.replace("-", "")
        list = self.db[store_id].find_one(local_str_time, {"_id": 0})
        if list is None:
            return False
        order_list = list['order_list']
        for order in order_list:
            if order['serial_num'] == serial_num:
                order['status'] = status
                # if status == 3:
                #     print order['money']
                #     self.db[store_id].update_one({"_id": local_str_time}, {"$inc": {'money_total': order['money']}})
                #     order['status'] = status
                #     break
                # else:
                #     order['status'] = status
                #     break
        self.db[store_id].update_one({'_id': local_str_time}, {"$set": {"order_list": order_list}})
        self.db['order_info'].update_one({'_id': serial_num},
                                         {"$set": {"status": status,"pay_serial_num":pay_serial_num}})
        return True

    def list_order(self, user_id, page, index):
        pages = (page - 1) * index
        list = self.db['order_info'].find({'consumer_id': user_id}, {"consumer_id":0,"business_id":0,"pay_serial_num":0}).sort("create_time",
                                                                                  direction=-1).skip(pages).limit(index)
        result = []
        for team in list:
            result.append(team)
        return result
        pass

    def find_order(self, id):
        result = self.db['order_info'].find_one(id,{"pay_serial_num":0})
        return result

    def dish_sales(self,store_id,dish):
        dish_info = self.db['business_info'].find_one(store_id, {'_id': 0, 'dish': 1})
        dish_list = dish_info['dish']
        for each in dish_list:
            for item in dish:
                if item['dish_name'] == each['dish_name']:
                    each['sales'] = each['sales'] + item['dish_count']
        self.db['business_info'].update_one({'_id':store_id},{'$set':{'dish':dish_list}})

if __name__ == "__main__":

    pass
