# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: mysql_updater.py
# @description: 将爬到本地的数据更新到MySQL

import pymysql
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.types import NVARCHAR, Float, Integer, Text

from config import username, password, database


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
    try:
        df.to_sql(name=table_name, con=con, if_exists='append', index=False, dtype=dtype_dict)
    except:
        print('[csv2mysql] Insert data repeatedly, skip.')


def recap2mysql(recap):
    dtype_dict = {
        recap.columns[0]: NVARCHAR(length=8),
        recap.columns[1]: NVARCHAR(length=64),
        recap.columns[2]: Text(),
        recap.columns[3]: NVARCHAR(length=32), 
        recap.columns[4]: NVARCHAR(length=256)
    }
    
    # 通过dtype设置类型 为dict格式{"col_name":type}
    try:
        recap.to_sql(name='recap', con=con, if_exists='append', index=False, dtype=dtype_dict)
    except:
        print('[recap2mysql] Insert data repeatedly, skip.')

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
    csv2mysql(player_score_stats, 'player_score_stats', 32)

    try:
        game_recap = pd.read_csv(path + 'game_recap.csv')
    except:
        print('[game2mysql] There was no game_recap in folder \'' + path + '\', skip.')
    else:
        recap2mysql(game_recap)


def futureGame2mysql(game):
    game = pd.DataFrame(game).T
    game['awayTeam'] = "nan"
    game['homeTeam'] = "nan"
    game['away_win_rate'] = 0.0
    game['home_win_rate'] = 0.0

    gameTeam = game.iloc[0]['gameTeam']
    gameTeam = gameTeam.split("vs")
    game['awayTeam'] = gameTeam[0]
    game['homeTeam'] = gameTeam[1]

    game.drop(columns=['gameOver','gameTeam'], axis=1, inplace=True)
    game['gameId'] = game['gameId'].astype(int)

    dtype_dict = {
        game.columns[0]: Integer(),
        game.columns[1]: NVARCHAR(length=32),
        game.columns[2]: NVARCHAR(length=3), 
        game.columns[3]: NVARCHAR(length=3), 
        game.columns[4]: Float(precision=6, asdecimal=True),
        game.columns[5]: Float(precision=6, asdecimal=True),
    }

    try:
        game.to_sql(name='future_game', con=con, if_exists='append', index=False, dtype=dtype_dict)
    except:
        print('[futureGame2mysql] game ' + str(game['gameId']) + ' has existed, skip.')


def dropFutureGame4mysql(gameId):
    # 打开数据库连接
    db = pymysql.connect("localhost", username, password, database)
    cursor = db.cursor()    # 使用cursor()方法获取操作游标 
    try:
        cursor.execute("DELETE FROM future_game where gameId=" + gameId)
        db.commit()
        print("[dropFutureGame4mysql] drop game: " + gameId + " from table future_game.")                  
    except:
        db.rollback()   # 发生错误时回滚
    db.close()


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
                if schedule.iloc[i]['gameOver']:
                    gameTeam = schedule.iloc[i]['gameTeam']
                    filepath = path + gameTeam + '/'
                    print(filepath)
                    game2mysql(filepath)
                    dropFutureGame4mysql(schedule.iloc[i]['gameId'])
                else:
                    # e.g. 2019-07-06
                    print('[schedule2mysql] Games were postponed, import into future_game table.')
                    futureGame2mysql(schedule.iloc[i])


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


def clear_mysql():
    # 打开数据库连接
    db = pymysql.connect("localhost", username, password, database)
    cursor = db.cursor()    # 使用cursor()方法获取操作游标 
    try:
        cursor.execute("drop table team;")
        cursor.execute("drop table game;")
        cursor.execute("drop table team_score_stats;")
        cursor.execute("drop table player_score_stats;")
        cursor.execute("drop table recap;")
        cursor.execute("drop table future_game;")
        db.commit()
        # print("Cleared tables in " + database)                  
    except:
        db.rollback()   # 发生错误时回滚
    db.close()


def set_default_primary():
    # 打开数据库连接
    db = pymysql.connect("localhost", username, password, database)
    cursor = db.cursor()    # 使用cursor()方法获取操作游标 
    try:
        # ALTER TABLE countryRiskLevel ADD PRIMARY KEY ( countrycd );
        cursor.execute("ALTER TABLE team ADD PRIMARY KEY (teamId);")
        cursor.execute("ALTER TABLE game ADD PRIMARY KEY (gameId);")
        cursor.execute("ALTER TABLE team_score_stats ADD PRIMARY KEY (id);")
        cursor.execute("ALTER TABLE player_score_stats ADD PRIMARY KEY (id);")
        cursor.execute("ALTER TABLE recap ADD PRIMARY KEY (gameId);")
        cursor.execute("ALTER TABLE future_game ADD PRIMARY KEY (gameId);")
        db.commit()
        # print("Cleared tables in " + database)                  
    except:
        db.rollback()   # 发生错误时回滚
    db.close()


if __name__ == "__main__":
    #path = './data/games/2019-12-22/ATLvsBKN/'
    #game2mysql(path)
    #team2mysql()
    #clear_mysql()
    #schedule2mysql()
    pass
