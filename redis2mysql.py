# _*_ coding:utf-8 _*_ 
_author_ = 'mlj'
_date_ = '2017/10/17 18:15'

import json
import redis
# py3 不支持MySQLdb
# from pymysql import *
# import MySQLdb
import pymysql


def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    # 指定mysql数据库
    mysqlcli =  pymysql.connect(host='127.0.0.1', user='root', passwd='mysql', db='Tianqi', port=3306, charset='utf8')
    # conn = connect(host='localhost', port=3306, database='test1', user='root', password='mysql', charset='utf8')
    while True:
        source, data = rediscli.blpop(['tian:items'])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            cur.execute("INSERT INTO tianqi(area, crawl_time, url, datetime, max_t, min_t, weather, wind_direction, wind_power) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )",
                        [item['area'], item['crawl_time'], item['url'],
                         item['datetime'], item['max_t'],item['min_t'], item['weather'], item['wind_direction'], item['wind_power']])
            mysqlcli.commit()
            cur.close()
            print('inserted %s'% item['source_url'])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

















