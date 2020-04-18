from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

from data_handler import map_team


def get_team_data(teamId, teamUrl):
    html = urlopen(teamUrl)
    soup = BeautifulSoup(html, features='lxml')
    # part-1
    team_data = soup.find('div', {'class': 'team_data'})

    teamName = team_data.find('span', {'class': 'title-text'}).get_text()
    logo_url = team_data.find('img')['src']
    description = team_data.find('div', {'class': 'txt'}).get_text().strip()
    # part-2
    content = team_data.find('div', {'class': 'font'}).get_text().split("\n")

    buildTime = content[1].split("：")[1]
    homeCourt = content[2].split("\xa0")[0].split("：")[1]
    area = content[2].split("\xa0")[1].split("：")[1]
    website = content[3].split("：")[1]
    chiefCoach = content[4].split("：")[1]
    
    team = {
        'teamId': teamId,
        'teamName': teamName,
        'buildTime': buildTime,
        'area': area,
        'homeCourt': homeCourt,
        'chiefCoach': chiefCoach,
        'logoUrl': logo_url,
        'website': website,
        'description': description
    }
    return team


def write_team_data(team_data):
    path = './data/teams/'
    team_data.to_csv(path + 'teams.csv', index=False, header=True)


def team_spider():
    url = 'https://nba.hupu.com/teams'
    html = urlopen(url)
    soup = BeautifulSoup(html, features='lxml')

    team_list = []
    content = soup.find_all('div', {'class': 'all'})
    for area in content:
        areaName = area.find('div', {'class': 'a'}).get_text()
        print(areaName)
        
        for team in area.find_all('a'):
            teamId = map_team(team.h2.get_text())
            teamUrl = team['href']
            print(teamId, teamUrl)
            team_data = get_team_data(teamId, teamUrl)
            team_list.append(team_data)

    team_df = pd.DataFrame(team_list)
    write_team_data(team_df)
    


if __name__ == "__main__":
    team_spider()

