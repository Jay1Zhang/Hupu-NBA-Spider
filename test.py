# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: test_spider.py
# @description: 测试爬虫

from schedule_spider import schedule_spider
from mysql_updater import schedule2mysql, clear_mysql
from data_generator import gen_dates_by_month

# '2019-02-21'   '2019-10-04'
#bug_date_list = ['2019-01-30', '2019-02-13', '2019-02-21', '2019-03-09', '2019-10-02', '2019-10-04']
#schedule_spider(bug_date_list)
clear_mysql()
schedule2mysql(gen_dates_by_month(2020, 4))

#schedule_spider(['2019-03-21'])
#date = gen_dates(2019)
#print(date[100:])