# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: .py
# @description: 调用者只需关注该类即可

import datetime

from data_generator import gen_dates_by_year
from schedule_spider import schedule_spider
from team_spider import team_spider
from mysql_updater import init_mysql, schedule2mysql


"""
    定义给外部的接口函数
"""
def spider_today():
    today = str(datetime.date.today())
    print(today)
    schedule_spider([today])
    schedule2mysql([today])


def spider_all():
    # 爬取队伍数据
    team_spider()
    # 爬取比赛数据
    dates = gen_dates_by_year(2019)[300:]
    schedule_spider(dates)
    # 初始化数据库
    init_mysql()


if __name__ == "__main__":
    #spider_all()
    spider_today()
