# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:48:48 2016

@author: pfenerty
"""

import pandas as pd
import json
import urllib2


# region Utils

def j2p(url, index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        response = opener.open(url)
    except Exception:
        print('Could not get Stats')
        return None
    else:
        data = json.loads(response.read())
        headers = data['resultSets'][index]['headers']
        rows = data['resultSets'][index]['rowSet']
        data_dict = [dict(zip(headers, row)) for row in rows]
        return pd.DataFrame(data_dict)


def getJson(url, index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    data = data['resultSets'][index]['rowSet']
    return data


def j2p2(url, index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    data_dict = [dict(zip(headers, row)) for row in rows]
    return pd.DataFrame(data_dict)


def get_year_string(year):
    return str(year) + "-" + str(year + 1)[2:4]


# endregion

# region Enums

# perModes = ["Totals", "PerPossession", "PerPlay", "PerMinute"]
perModes = ["Totals", "PerPossession"]
# seasonTypes = ["Pre+Season", "Regular+Season", "Playoffs", "All+Star"]
seasonTypes = ["Regular+Season", "Playoffs"]
# measureTypes = ["Base", "Advanced", "Misc", "Scoring", "Usage", "Opponent", "Defense"]
measureTypes = ["Base", "Advanced"]
years = range(1996, 2015)


# endregion

# region Base Stats


def get_stat_csv(team_or_player, measure_type, per_mode, season_year, season_type):
    url = "http://stats.nba.com/stats/leaguedash{teamOrPlayer}stats?College=&Conference=&Country=&DateFrom=" \
          "&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0" \
          "&LeagueID=00&Location=&MeasureType={measureType}&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
          "&PaceAdjust=N&PerMode={perMode}&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N" \
          "&Rank=N&Season={seasonYear}&SeasonSegment=&SeasonType={seasonType}&ShotClockRange=&StarterBench=" \
          "&TeamID=0&VsConference=&VsDivision=&Weight="
    url = url.format(perMode=per_mode, seasonYear=season_year, seasonType=season_type, measureType=measure_type,
                     teamOrPlayer=team_or_player)
    df = j2p(url, 0)
    if df is not None:
        df.to_csv("data" + "\\" + team_or_player + "\\" + measure_type + "\\" + season_type + "\\" + per_mode + "\\" +
                  season_year + ".csv")


def get_all_player_stats():
    for year in years:
        year_string = get_year_string(year)
        for measure_type in measureTypes:
            for season_type in seasonTypes:
                for per_mode in perModes:
                    print(year_string + ": " + measure_type + ", " + season_type + ", " + per_mode)
                    get_stat_csv("player", measure_type, per_mode, year_string, season_type)


# endregion

# region Shot Location Stats


def get_shot_location_stats(player_or_team, measure_type, per_mode, season_year, season_type):
    url = "http://stats.nba.com/stats/leaguedash{playerOrTeam}shotlocations?College=&Conference=&Country=&DateFrom=" \
          "&DateTo=&DistanceRange=5ft+Range&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=" \
          "&LastNGames=0&LeagueID=00&Location=&MeasureType={measureType}&Month=0&OpponentTeamID=0&Outcome=&PORound=0" \
          "&PaceAdjust=N&PerMode={perMode}&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N" \
          "&Season={seasonYear}&SeasonSegment=&SeasonType={seasonType}&ShotClockRange=&StarterBench=&TeamID=0" \
          "&VsConference=&VsDivision=&Weight="
    url = url.format(playerOrTeam=player_or_team, measureType=measure_type, perMode=per_mode, seasonYear=season_year,
                     seasonType=season_type)
    df = j2p(url, 0)
    if df is not None:
        df.to_csv("data\\" + player_or_team + "\\" + measure_type + "\\" + season_type + "\\" + per_mode + "\\" +
                  season_year + ".csv")


def get_all_player_shot_location_stats():
    for year in years:
        year_string = get_year_string(year)
        for measure_type in measureTypes:
            for season_type in seasonTypes:
                for per_mode in perModes:
                    print(year_string + ": " + measure_type + ", " + season_type + ", " + per_mode)
                    get_shot_location_stats("player", measure_type, per_mode, year_string, season_type)


# endregion

# region SportsVU

sports_vu_types = ["CatchShoot", "Defense", "Drives", "Passing", "Possessions", "Rebounding", "PullUpShot",
                   "ElbowTouch", "PostTouch", "PaintTouch"]


def get_sports_vu_stats(player_or_team, vu_type, per_mode, season_year, season_type):
    url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0" \
          "&OpponentTeamID=0&Outcome=&PORound=0&PerMode={perMode}&PlayerExperience=&PlayerOrTeam={playerOrTeam}" \
          "&PlayerPosition=&PtMeasureType={vuType}&Season={seasonYear}&SeasonSegment=&SeasonType={seasonType}" \
          "&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    url = url.format(playerOrTeam=player_or_team, vuType=vu_type, seasonYear=season_year, seasonType=season_type,
                     perMode=per_mode)
    df = j2p(url, 0)
    if df is not None:
        df.to_csv(
            "data\\" + player_or_team + "\\" + vu_type + "\\" + season_type + "\\" + per_mode + "\\" + season_year)


def get_all_sports_vu_stats():
    for year in range(2013, 2015):
        year_string = get_year_string(year)
        for vu_type in sports_vu_types:
            for season_type in seasonTypes:
                for per_mode in perModes:
                    print(year_string + ": " + vu_type + ", " + season_type + ", " + per_mode)
                    get_sports_vu_stats("player", vu_type, per_mode, year_string, season_type)

# endregion
