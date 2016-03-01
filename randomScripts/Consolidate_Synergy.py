# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:36:18 2015

@author: Patrick
"""

import pandas as pd
from json2pandas import json2pandas as j2p

#player_tracking_shot_logs_url = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID="+player_id+"&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="
play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup","OffRebound","PRRollMan","Spotup","Transition"]
url_template="http://stats.nba.com/js/data/playtype/team_{play_type}.js"
    
synergy_full = pd.DataFrame()
for i in range(len(play_types)):
    play_type_data = j2p(url_template.format(play_type=play_types[i]),0)
    play_type_data = play_type_data[["TeamIDSID","TeamName","Poss","Points","PPP"]]
    play_type_data.columns = ["TeamIDSID","TeamName",play_types[i]+"_Poss",play_types[i]+"_Points",play_types[i]+"_PPP"]
    if i==0:
        synergy_full = play_type_data
    else:
        synergy_full = pd.merge(synergy_full,play_type_data,on=["TeamIDSID","TeamName"],how="outer")
        
team_adv_url="http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
team_adv_df = j2p(team_adv_url,0)
team_adv_df = team_adv_df[["TEAM_ID","OFF_RATING"]]
team_adv_df.columns = ["TeamIDSID","ORtg"]

results_df = pd.merge(synergy_full, team_adv_df)
corr = results_df.corr()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    