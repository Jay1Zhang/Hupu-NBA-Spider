# -*- coding: utf-8 -*-
# @Time    : 2020/04/18 21:30
# @Author  : jyz
# @FileName: data_handler.py
# @description: 数据清洗

team_map = {
    # 西部赛区
    "火箭": "HOU", "独行侠": "DAL", "灰熊": "MEM", "鹈鹕": "NOP", "鹈鹕": "NOP", "马刺": "SAS",
    # 太平洋赛区
    "湖人": "LAL", "快船": "LAC", "国王": "SAC", "太阳": "PHX", "勇士": "GSW",
    # 西北赛区
    "掘金": "DEN", "爵士": "UTA", "雷霆": "OKC", "开拓者": "POR", "森林狼": "MIN",
    # 大西洋赛区
    "猛龙": "TOR", "凯尔特人": "BOS", "76人": "PHI", "篮网": "BKN", "尼克斯": "NYK",
    # 东南赛区
    "热火": "MIA", "魔术": "ORL", "奇才": "WAS", "黄蜂": "CHA", "老鹰": "ATL",
    # 中部赛区
    "雄鹿": "MIL", "步行者": "IND", "公牛": "CHI", "活塞": "DET", "骑士": "CLE"
}

stats_title_map = {
    0: 'teamId', 1: 'teamStatsId', 
    2: 'playerName', 3: 'position', 4: 'playMinute', 
    5: 'shot', 6: 'threeShot', 7: 'penaltyShot', 8: 'frontCourt', 9: 'backCourt', 10: 'rebound', 
    11: 'assist', 12: 'foul', 13: 'steal', 14: 'fault', 15: 'block', 16: 'score', 17: 'Contribution'
}


def map_team_vs_team(team_str):
    # 检查赛程信息中的球队是否存在于map表中
    team_a = team_str.split("vs")[0]
    team_b = team_str.split("vs")[1]
    if team_a not in team_map.keys() or team_b not in team_map.keys():
        return None
    
    return map_team(team_str)


def map_team(team_str):
    for key, val in team_map.items():
        team_str = team_str.replace(key, val)
    return team_str


def format_player_stats(df, team_score_stats_id):
    # 重置标题行
    df.rename(columns=(stats_title_map), inplace=True)
    # 删除无用行
    df.drop(df.index[[0, 6, -2, -1]], inplace=True)
    # 利用team_score_stats_id生成id字段，并插入
    # 注意要先删除无用行再生成id，否则id将不连续
    df.insert(0, 'id', 0)
    df['id'] = [team_score_stats_id + "%02d" % (i+1) for i in range(len(df))]
    # 插入首发字段
    df.insert(4, 'isFirst', 0)
    df.loc[1:5, 'isFirst'] = 1
    
    return df


if __name__ == "__main__":
    str = "开赛：2019年04月11日 08:00"
    print(str.split('：')[1])

    print(map_team('公牛vs火箭'))

    