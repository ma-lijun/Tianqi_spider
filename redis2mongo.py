# _*_ coding:utf-8 _*_ 
_author_ = 'mlj'
_date_ = '2017/10/17 1:01'

import redis
from pymongo import MongoClient
import json

# 链接redis数据库
redis_cli = redis.Redis(host='127.0.0.1', port=6379, db=0)

# 链接mongo
mongo_cli = MongoClient('127.0.0.1', 27017)
db = mongo_cli['Tianqi']
col = db['tianqi']

while True:
    # 从redis中读取数据
    source, data = redis_cli.blpop(['tian:items'])
    print("---------")
    dict_data=dict(json.loads(data.decode()))

    # 写入mongodb
    col.insert(dict_data)