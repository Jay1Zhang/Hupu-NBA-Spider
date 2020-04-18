from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os

from data_generator import gen_dates_by_year
from data_handler import map_teams
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
        print('There were no games on ' + date + ', skip.')
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
            game_team = map_teams("".join(game_team.split()))
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
        print('\nWarning! Schedule-folder \'' + path + date + '\' already exists, and data will be overwritten.')
    
    df = pd.DataFrame(schedule)
    df.to_csv(path + date + '/' + date + '-schedule.csv', index=False)


def schedule_spider(dates):
    path = './data/games/'
    all_schedule = []
    for date in dates:
        schedule = get_schedule(date=date)      # 获取赛程信息
        if schedule is None:
            continue
        
        write_schedule(schedule, date=date)     # 写入文件
        all_schedule += schedule                

        for game in schedule:
            print(game['gameId'], game['gameTime'], game['gameTeam'], game['gameOver'])
            game_spider(path=path + date + '/', game=game)
        
    df = pd.DataFrame(all_schedule)
    df.to_csv(path + 'all_schedule.csv', index=False)    # 写入所有赛程信息


def main():
    schedule_spider(gen_dates_by_year(2019)[300:])


if __name__ == "__main__":
    main()    
