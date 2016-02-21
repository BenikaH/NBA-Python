# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:36:18 2015

@author: Patrick
"""

import pandas as pd
from json2pandas import json2pandas as j2p
import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
import numpy as np

#player_tracking_shot_logs_url = "http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID="+player_id+"&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="
play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup","OffRebound","PRRollMan","Spotup","Transition"]
url_template="http://stats.nba.com/js/data/playtype/team_{play_type}.js"
    
synergy_full = pd.DataFrame()
for i in range(len(play_types)):
    play_type_data = j2p(url_template.format(play_type=play_types[i]),0)
    play_type_data = play_type_data[["TeamIDSID","TeamName","Time","PPP"]]
    play_type_data.columns = ["TeamIDSID","TeamName",play_types[i]+"_Freq",play_types[i]+"_PPP"]
    if i==0:
        synergy_full = play_type_data
    else:
        synergy_full = pd.merge(synergy_full,play_type_data,on=["TeamIDSID","TeamName"],how="outer")
        
team_adv_url="http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
team_adv_df = j2p(team_adv_url,0)
team_adv_df = team_adv_df[["TEAM_ID","OFF_RATING"]]
team_adv_df.columns = ["TeamIDSID","ORtg"]

results_df = pd.merge(synergy_full, team_adv_df)   

cf.set_config_file(offline=False, world_readable=True, theme='ggplot')
synergy_full.iplot(kind='barh',barmode='stack', bargap=.1, filename='team_synergy_bar')

PNR_Ball_Handler = go.Box(
    y = synergy_full['PRBallHandler_Freq'],
    name = "PNR Ball Handler",
    hoverinfo = "text"
    )
    
Cut = go.Box(
    y = synergy_full['Cut_Freq'],
    name = "Cut",
    )
    
Handoff = go.Box(
    y = synergy_full['Handoff_Freq'],
    name = "Handoff"    
    )

Isolation = go.Box(
    y = synergy_full['Misc_Freq'],
    name = "Isolation"
    )

Misc = go.Box(
    y = synergy_full['Misc_Freq'],
    name = "Miscellaneous"
    )

Off_Screen = go.Box(
    y = synergy_full['OffScreen_Freq'],
    name = "Off Screen"
    )

Post_Up = go.Box(
    y = synergy_full['Postup_Freq'],
    name = "Post Up"
    )

Off_Rebound = go.Box(
    y = synergy_full['OffRebound_Freq'],
    name = "Offensive Rebound"
    )    
    
PNR_Roll_Man = go.Box(
    y = synergy_full['PRRollMan_Freq'],
    name = "PNR Roll Man"
    )

Spot_Up = go.Box(
    y = synergy_full['Spotup_Freq'],
    name = "Spot Up"
    )
    
Transition = go.Box(
    y = synergy_full['Transition_Freq'],
    name = "Transition"
    )
    
data = [PNR_Ball_Handler,Cut,Handoff,Isolation,Misc,Off_Screen,Post_Up,Off_Rebound,PNR_Roll_Man,Spot_Up,Transition]
plot_url = py.plot(data, filename='team_synergy_box')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    