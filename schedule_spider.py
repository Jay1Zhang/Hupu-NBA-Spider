# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: schedule_spider.py
# @description: 爬取所有赛程相关信息

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
import random
import time

from data_generator import gen_dates_by_year
from data_handler import map_team_vs_team
from game_spider import game_spider


schedule_url = 'https://nba.hupu.com/schedule/'


def get_schedule(date):
    # e.g. date='2020-03-01'
    def check_data(players_table):
        if players_table is None:
            return False

        day = players_table.find('tr', {'class': 'left linglei'}).get_text().strip()[3:5]
        if day != date.split('-')[2]:
            # 验证期望的date与抓取到的game_date是否一致
            return False

        return True
    
    url = schedule_url + date
    html = urlopen(url)
    soup = BeautifulSoup(html, features='lxml')
    players_table = soup.find("table", {"class": "players_table"})
    if not check_data(players_table):
        print('[get_schedule] There were no games on ' + date + ', skip.')
        return None
    
    game_date = None
    schedule = []
    for tr in players_table.find_all("tr", {"class": "left"}):
        if "linglei" in tr.attrs['class']:
            if game_date:
                break
            game_date = tr.get_text().strip()
        else:
            td_list = tr.find_all("td")
            game_time = date + ' ' + td_list[0].get_text()
            game_team = td_list[1].get_text()
            game_team = map_team_vs_team("".join(game_team.split()))
            # 遇到某些已被剔除的球队，直接跳过，如 2019-02-21 北卡vs杜克
            if game_team is None:
                continue
            #game_team = "".join(game_team.split())
            #game_team = map_team(game_team)
            game_data = td_list[2].a['href'].split('/')[-1]
            game_over = int(td_list[2].a.get_text() == '数据统计')
            
            schedule.append({'gameId': game_data,
                             'gameTime': game_time, 
                             'gameTeam': game_team, 
                             'gameOver': game_over})
    
    return schedule


def write_schedule(schedule, date, path='./data/games/'):
    if schedule is None:
        return 

    try:
        os.mkdir(path + date)
    except:
        print('\n[write_schedule] Warning! Schedule-folder \'' + path + date + '\' already exists, and data will be overwritten.')
    
    df = pd.DataFrame(schedule)
    df.to_csv(path + date + '/' + date + '-schedule.csv', index=False)


def schedule_spider(dates):
    path = './data/games/'
    all_schedule = []
    cnt = 0
    for date in dates:
        """sleep"""
        cnt += 1
        if cnt == 15:
            # 每爬取30天的赛程强行休息一分钟
            cnt = 0
            time.sleep(60)
        # 随机一段时间休眠
        sleep_time = round(random.random(),4)
        time.sleep(sleep_time)
        """sleep"""
        # 获取赛程信息
        schedule = get_schedule(date=date)      
        if schedule is None:
            continue
        
        write_schedule(schedule, date=date)     # 写入文件
        all_schedule += schedule                

        for game in schedule:
            print('[schedule_spider]', game['gameId'], game['gameTime'], game['gameTeam'], game['gameOver'])
            game_spider(path=path + date + '/', game=game)
        
    df = pd.DataFrame(all_schedule)
    if os.path.isfile(path + 'all_schedule.csv'):
        df.to_csv(path + 'all_schedule.csv', index=False, header=False, mode='a')    # 补充写入
    else:
        df.to_csv(path + 'all_schedule.csv', index=False, header=True)    # 写入所有赛程信息


def main():
    schedule_spider(gen_dates_by_year(2019)[364:])


if __name__ == "__main__":
    main()    
