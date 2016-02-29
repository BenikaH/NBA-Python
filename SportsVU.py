# -*- coding: utf-8 -*-
"""
Created on Fri Feb 05 12:41:58 2016

@author: pfenerty
"""

from json2pandas import json2pandas as j2p
import pandas as pd

SVU_url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType={SVU_type}&Season={year}&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
team_adv_url="http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={year}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
SVU_types = ["CatchShoot","Defense","Drives","Passing","PullUpShot","Rebounding","SpeedDistance","ElbowTouch","PostTouch","PaintTouch"]
years = ["2013-14","2014-15","2015-16"]

SVU_df = pd.DataFrame
team_adv_df = pd.DataFrame
for i,year in enumerate(years):
    print(year)
    yearly_SVU_df = pd.DataFrame
    for j,svu_type in enumerate(SVU_types):
        type_url = SVU_url.format(SVU_type=svu_type,year=year)
        type_df = j2p(type_url,0)
        type_df = type_df.drop(['GP','W','L','MIN','TEAM_ABBREVIATION'],1)
        type_df['Year'] = year[0:4]
        if j == 0:
            yearly_SVU_df = type_df
        else:
            yearly_SVU_df = pd.merge(yearly_SVU_df, type_df, on=["TEAM_ID","TEAM_NAME","Year"],how="outer")
    if i == 0:
        SVU_df = yearly_SVU_df
    else:
        SVU_df =SVU_df.append(yearly_SVU_df,ignore_index=True)
    yearly_adv_url = team_adv_url.format(year=year)
    yearly_adv_df = j2p(yearly_adv_url,0)
    yearly_adv_df = yearly_adv_df[["TEAM_ID","OFF_RATING","DEF_RATING", "PACE"]]
    yearly_adv_df.columns = ["TEAM_ID","ORtg","DRtg","Pace"]
    yearly_adv_df['Year'] = year[0:4]
    if i == 0:
        team_adv_df = yearly_adv_df
    else:
        team_adv_df=team_adv_df.append(yearly_adv_df,ignore_index=True)

result_df = pd.merge(SVU_df, team_adv_df, on=["TEAM_ID","Year"], how="outer")
result_df.to_csv("SportsVU.csv")
ortg_corr = result_df.corr()['ORtg']
drtg_corr = result_df.corr()['DRtg']