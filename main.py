# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: main.py
# @description: 调用者只需关注该类即可

import os
import shutil
import datetime
import pandas as pd

from data_generator import gen_dates_by_year, gen_dates_by_month
from schedule_spider import schedule_spider
from team_spider import team_spider
from mysql_updater import team2mysql, schedule2mysql, game2mysql, clear_mysql, set_default_primary


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

"""
    初始化data文件夹，该操作非常危险，保证只执行一次
"""
def init_dir():
    shutil.rmtree('./data')

    os.mkdir('./data')
    os.mkdir('./data/games')
    os.mkdir('./data/teams')
    os.mkdir('./data/players')

"""
    初始化MySQL数据库，保证在数据库为空时执行且仅执行一次。
"""
def init_mysql():
    # 清空数据库
    clear_mysql()
    # 初始化队伍数据
    team2mysql()
    # 初始化比赛数据
    path = './data/games/'
    all_schedule = pd.read_csv(path + 'all_schedule.csv')
    all_schedule.drop_duplicates()

    for i in range(0, len(all_schedule)):
        gameTime = all_schedule.iloc[i]['gameTime'].split(" ")[0]
        gameTeam = all_schedule.iloc[i]['gameTeam']
        filepath = path + gameTime + '/' + gameTeam + '/'
        print(filepath)
        game2mysql(filepath)

    # 手动设置各表的主键
    set_default_primary()

"""
    爬取所有数据，保证只执行一次
"""
def init_data():
    # 爬取队伍数据
    team_spider()
    # 爬取比赛数据
    if os.path.exists('./data/games/all_schedule.csv'):
        # 初始化数据库时
        os.remove('./data/games/all_schedule.csv')
    
    #dates = gen_dates_by_year(2019)
    dates = gen_dates_by_month(2019, 1)
    schedule_spider(dates)

"""
    初始化操作，保证只执行一次
"""
def init_all():
    init_dir()      # 清空data文件夹
    init_data()     # 爬取所有数据到本地
    init_mysql()    # 初始化数据库


if __name__ == "__main__":
    #init_all()  # 1
    update_dates(gen_dates_by_month(2019, 2))   # 2~12
    #update_today()
    #init_mysql()
    #clear_mysql()
