# 西部赛区
team_map = {
    "火箭": "HOU",
    "独行侠": "DAL",
    "灰熊": "MEM",
    "鹈鹕": "NOP",
    "鹈鹕": "NOP",
    "马刺": "SAS",
    # 太平洋赛区
    "湖人": "LAL",
    "快船": "LAC",
    "国王": "SAC",
    "太阳": "PHX",
    "勇士": "GSW",
    # 西北赛区
    "掘金": "DEN",
    "爵士": "UTA",
    "雷霆": "OKC",
    "开拓者": "POR",
    "森林狼": "MIN",
    # 大西洋赛区
    "猛龙": "TOR",
    "凯尔特人": "BOS",
    "76人": "PHI",
    "篮网": "BKN",
    "尼克斯": "NYK",
    # 东南赛区
    "热火": "MIA",
    "魔术": "ORL",
    "奇才": "WAS",
    "黄蜂": "CHA",
    "老鹰": "ATL",
    # 中部赛区
    "雄鹿": "MIL",
    "步行者": "IND",
    "公牛": "CHI",
    "活塞": "DET",
    "骑士": "CLE"
}

def map_team(team_str):
    for key, val in team_map.items():
        team_str = team_str.replace(key, val)
    return team_str

"""
def replace_team(team_str):
    # 西部赛区
    team_str = team_str.replace("火箭", "HOU")
    team_str = team_str.replace("独行侠", "DAL")
    team_str = team_str.replace("灰熊", "MEM")
    team_str = team_str.replace("鹈鹕", "NOP")
    team_str = team_str.replace("鹈鹕", "NOP")
    team_str = team_str.replace("马刺", "SAS")
    # 太平洋赛区
    team_str = team_str.replace("湖人", "LAL")
    team_str = team_str.replace("快船", "LAC")
    team_str = team_str.replace("国王", "SAC")
    team_str = team_str.replace("太阳", "PHX")
    team_str = team_str.replace("勇士", "GSW")
    # 西北赛区
    team_str = team_str.replace("掘金", "DEN")
    team_str = team_str.replace("爵士", "UTA")
    team_str = team_str.replace("雷霆", "OKC")
    team_str = team_str.replace("开拓者", "POR")
    team_str = team_str.replace("森林狼", "MIN")
    # 大西洋赛区
    team_str = team_str.replace("猛龙", "TOR")
    team_str = team_str.replace("凯尔特人", "BOS")
    team_str = team_str.replace("76人", "PHI")
    team_str = team_str.replace("篮网", "BKN")
    team_str = team_str.replace("尼克斯", "NYK")
    # 东南赛区
    team_str = team_str.replace("热火", "MIA")
    team_str = team_str.replace("魔术", "ORL")
    team_str = team_str.replace("奇才", "WAS")
    team_str = team_str.replace("黄蜂", "CHA")
    team_str = team_str.replace("老鹰", "ATL")
    # 中部赛区
    team_str = team_str.replace("雄鹿", "MIL")
    team_str = team_str.replace("步行者", "IND")
    team_str = team_str.replace("公牛", "CHI")
    team_str = team_str.replace("活塞", "DET")
    team_str = team_str.replace("骑士", "CLE")
    
    return team_str
"""

if __name__ == "__main__":
    str = "开赛：2019年04月11日 08:00"
    print(str.split('：')[1])

    