from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
import pandas as pd
import re
import os


def get_game_pros():
    # 尚未开始的比赛，比赛前瞻
    pass


def get_game_base_info(game, game_id):
    game_base_info = game.find('div', {'class': 'about_fonts clearfix'})
    
    gameTime = game_base_info.find('p', {'class': 'time_f'}).get_text().split('：')[1]
    consumTime = game_base_info.find('p', {'class': 'consumTime'}).get_text().split('：')[1]
    arena = game_base_info.find('p', {'class': 'arena'}).get_text().split('：')[1]
    peopleNum = game_base_info.find('p', {'class': 'peopleNum'}).get_text().split('：')[1]
    
    base_info = {'gameId': game_id, 'gameTime': gameTime, 
                 'consumTime': consumTime, 'arena': arena, 'peopleNum': peopleNum}
    return pd.DataFrame([base_info])

    
def get_game_score_info(game):
    def _get_team_score_info(is_home_team):
        # 获取球队基本信息
        team_id = 'team_b' if is_home_team else 'team_a'
        team = game.find('div', {'class': team_id})

        name = team.find('p').get_text().strip()
        msg = team.find('div', {'class': 'message'}).find('div').get_text().strip()
        link = team.find('p').a['href']

        # 获取比分情况
        team_id = 'home_score' if is_home_team else 'away_score'
        score_tag = game.find('tr', {'class': 'away_score'}).find_all('td')
        if len(score_tag) < 6:
            # 缺失数据
            score1, score2, score3, score4, score = None, None, None, None, None
        else:
            score1 = score_tag[1].get_text().strip()
            score2 = score_tag[2].get_text().strip()
            score3 = score_tag[3].get_text().strip()
            score4 = score_tag[4].get_text().strip()
            score = score_tag[5].get_text().strip()

        return {'队名': name, '基本信息': msg, 
                 '一': score1, '二': score2, '三': score3, '四': score4, '总分': score,
                 '球队链接': link, }

    away_team = _get_team_score_info(is_home_team=False)
    home_team = _get_team_score_info(is_home_team=True)
    
    return pd.DataFrame([away_team, home_team])


def get_team_score_table(game, is_home_team):
    team_id = 'J_home_content' if is_home_team else 'J_away_content'
    
    table = []
    for tr in game.find('table', {'id': team_id}).find_all('tr'):
        line = [td.get_text().strip() for td in tr.find_all('td')]
        table.append(line)
    
    df = pd.DataFrame(table)
    df.iloc[0,1] = "位置"
    return df


def get_game_recap(game):
    recap_url = game.find('a', {'class': 'a', 'target': '_self'})['href']
    html = urlopen(recap_url)
    soup = BeautifulSoup(html, features='lxml')
    
    recap = soup.find('div', {'class': 'news_box'})
    try:
        header = recap.find('h2').get_text()
        content = recap.find('div', {'class': 'content'}).get_text().strip()
        upd_time = recap.find('div', {'class': 'time'}).get_text().split('：')[-1]
        
        img_url = recap.find('img')['src']
    except:
        print('\tThere was no report of the game.')
        return None
    else:
        return pd.DataFrame([{'标题': header, '内容': content, '更新时间': upd_time, '精彩瞬间': img_url}])


def get_game_data(game_id):
    # 已经结束的比赛，数据统计
    boxscore_url = 'https://nba.hupu.com/games/boxscore/'
    url = boxscore_url + game_id
    
    html = urlopen(url)
    soup = BeautifulSoup(html, features='lxml')
    
    game = soup.find('div', {'class': 'gamecenter_content_l'})
    game_base_info = get_game_base_info(game, game_id)
    game_score_info = get_game_score_info(game)
    away_team_score_table = get_team_score_table(game, is_home_team=False)
    home_team_score_table = get_team_score_table(game, is_home_team=True)
    game_recap = get_game_recap(game)

    return game_base_info, game_score_info, away_team_score_table, home_team_score_table, game_recap


def write_game_data(path, dir_name, 
                    game_base_info, game_score_info, 
                    away_team_score_table, home_team_score_table,
                    game_recap):
    try:
        os.mkdir(path + dir_name)
    except:
        print('\tWarning! Game-folder \'' + path + dir_name + '\' already exists, and data will be overwritten.')
    
    game_base_info.to_csv(path + dir_name + '/game_base_info.csv', index=False, header=True)
    game_score_info.to_csv(path + dir_name + '/game_score_info.csv', index=False, header=True)
    away_team_score_table.to_csv(path + dir_name + '/away_team_score_table.csv', index=False, header=False)
    home_team_score_table.to_csv(path + dir_name + '/home_team_score_table.csv', index=False, header=False)
    if game_recap is not None:
        game_recap.to_csv(path + dir_name + '/game_recap.csv', index=False)
        #urlretrieve(game_recap.loc[0, '精彩瞬间'], path + dir_name + '/capture.jpg')
        

def game_spider(path, game):
    if game['gameOver']:
        # 比赛已经结束, 做技术统计
        base, score, away, home, recap = get_game_data(game['gameId'])
        write_game_data(path, game['gameTeam'], 
                        base, score, away, home, recap)
    else:
        # 比赛尚未开始，做比赛前瞻
        pass   


def main():
    pass


if __name__ == "__main__":
    main()    
