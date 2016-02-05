# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:33:39 2015

@author: pjfenert
"""
import pandas as pd
from json2pandas import json2pandas
    
team_adv_url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
temp_df = json2pandas(team_adv_url,0)
passing_df = pd.DataFrame(columns={"TeamID","Team Name","Offensive Rating","Pace","PassesPerPossession"})
passing_df["TeamID"] = temp_df["TEAM_ID"]
passing_df["Team Name"] = temp_df["TEAM_NAME"]
passing_df["Offensive Rating"] = temp_df["OFF_RATING"]
passing_df["Pace"] = temp_df["PACE"]
team_pass_url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=Passing&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
temp_df = json2pandas(team_pass_url,0)
temp_df2 = pd.DataFrame(columns={"TeamID","Team Name","PassesPerGame"})
temp_df2["TeamID"] = temp_df["TEAM_ID"]
temp_df2["Team Name"] = temp_df["TEAM_NAME"]
temp_df2["PassesPerGame"] = temp_df["PASSES_MADE"]
passing_df = pd.merge(passing_df,temp_df2, on=["TeamID","Team Name"], how="outer")
for index, row in passing_df.iterrows():
    passing_df.loc[index,'PassesPerPossession'] = row.PassesPerGame / row.Pace
    
print(passing_df.corr())
