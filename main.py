# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: main.py
# @description: 调用者只需关注该类即可

import datetime

from data_generator import gen_dates_by_year
from schedule_spider import schedule_spider
from team_spider import team_spider
from mysql_updater import init_mysql, schedule2mysql


"""
    定义给外部的接口函数
"""
def update_dates(dates):
    schedule_spider(dates)
    schedule2mysql(dates)


def update_today():
    today = str(datetime.date.today())
    print(today)
    schedule_spider([today])
    schedule2mysql([today])


def init_all():
    # 爬取队伍数据
    team_spider()
    # 爬取比赛数据
    dates = gen_dates_by_year(2019)[300:]
    schedule_spider(dates)
    # 初始化数据库
    init_mysql()


if __name__ == "__main__":
    #init_all()
    #update_today()
    update_dates(['2019-02-21'])
