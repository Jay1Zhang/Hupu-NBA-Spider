# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: mysql_updater.py
# @description: 将爬到本地的数据更新到MySQL

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.types import NVARCHAR, Float, Integer, Text


username = 'root'
password = 'ur_password'
database = 'project_Hupu'

engine = create_engine('mysql+pymysql://' + username + ':' + password + '@127.0.0.1/' + database)
#engine = create_engine('mysql+pymysql://root:password@127.0.0.1/project_Hupu')
# 建立连接
con = engine.connect()

def csv2mysql(df, table_name, length):
    dtype_dict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtype_dict.update({i: NVARCHAR(length=length)})
        if "float" in str(j):
            dtype_dict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtype_dict.update({i: Integer()})
    
    # 通过dtype设置类型 为dict格式{“col_name”:type}
    df.to_sql(name=table_name, con=con, if_exists='append', index=False, dtype=dtype_dict)


def recap2mysql(recap):
    dtype_dict = {
        recap.columns[0]: NVARCHAR(length=8),
        recap.columns[1]: NVARCHAR(length=64),
        recap.columns[2]: Text(),
        recap.columns[3]: NVARCHAR(length=32), 
        recap.columns[4]: NVARCHAR(length=256)
    }
    
    # 通过dtype设置类型 为dict格式{"col_name":type}
    recap.to_sql(name='recap', con=con, if_exists='append', index=False, dtype=dtype_dict)


"""
    将指定比赛的数据更新到MySQL
"""
def game2mysql(path):
    # 读取df
    game_base_info = pd.read_csv(path + 'game_base_info.csv')
    team_score_stats = pd.read_csv(path + 'team_score_stats.csv')
    player_score_stats = pd.read_csv(path + 'player_score_stats.csv')

    # df2sql
    csv2mysql(game_base_info, 'game', 32)
    csv2mysql(team_score_stats, 'team_score_stats', 8)
    csv2mysql(player_score_stats, 'player_score_stats', 16)

    try:
        game_recap = pd.read_csv(path + 'game_recap.csv')
    except:
        print('[game2mysql] There was no game_recap in folder \'' + path + '\', skip.')
    else:
        recap2mysql(game_recap)

"""
    将指定日期的所有比赛数据更新到MySQL
"""
def schedule2mysql(dates):
    for date in dates:
        path = './data/games/' + date + '/'
        try:
            schedule = pd.read_csv(path + date + '-schedule.csv')
        except:
            print('[schedule2mysql] There were no games on ' + date + ', skip.')
        else:
            for i in range(0, len(schedule)):
                gameTeam = schedule.iloc[i]['gameTeam']
                filepath = path + gameTeam + '/'
                print(filepath)
                game2mysql(filepath)


def team2mysql():
    teams = pd.read_csv('./data/teams/teams.csv')

    dtype_dict = {}
    for i, j in zip(teams.columns, teams.dtypes):
        if "object" in str(j):
            dtype_dict.update({i: NVARCHAR(length=32)})
        if "float" in str(j):
            dtype_dict.update({i: Float(precision=2, asdecimal=True)})
        if "int" in str(j):
            dtype_dict.update({i: Integer()})
    
    dtype_dict.update({'logoUrl': NVARCHAR(length=64), 'website': NVARCHAR(length=64), 'description': Text()})
    print(dtype_dict)
    # 通过dtype设置类型 为dict格式{“col_name”:type}
    teams.to_sql(name='team', con=con, if_exists='replace', index=False, dtype=dtype_dict)


"""
    初始化MySQL数据库，保证在数据库为空时执行且仅执行一次。
"""
def init_mysql():
    # 初始化队伍数据
    team2mysql()
    # 初始化比赛数据
    path = './data/games/'
    all_schedule = pd.read_csv(path + 'all_schedule.csv')

    for i in range(0, len(all_schedule)):
        gameTime = all_schedule.iloc[i]['gameTime'].split(" ")[0]
        gameTeam = all_schedule.iloc[i]['gameTeam']
        filepath = path + gameTime + '/' + gameTeam + '/'
        print(filepath)
        game2mysql(filepath)


if __name__ == "__main__":
    #path = './data/games/2019-12-22/ATLvsBKN/'
    #game2mysql(path)
    #team2mysql()
    #init_mysql()
    schedule2mysql(['2019-12-30', '2019-12-31'])
