# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:33:39 2015

@author: pjfenert
"""
import pandas as pd
from json2pandas import json2pandas as j2p
import plotly.plotly as py
import cufflinks as cf
import plotly.graph_objs as go
    
team_adv_url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
adv = j2p(team_adv_url,0)
adv = adv[['TEAM_ID','PACE','EFG_PCT']]
team_pass_url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=Passing&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
passing = j2p(team_pass_url,0)
passing = passing[['TEAM_ID','PASSES_MADE']]
SVU_poss_url="http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=Possessions&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
poss = j2p(SVU_poss_url,0)
poss = poss[['TEAM_ID','TEAM_NAME','TIME_OF_POSS']]
df = pd.merge(adv,passing,on=['TEAM_ID'],how="inner")
df = pd.merge(df,poss,on=['TEAM_ID'],how="inner")
df['Seconds Per Possession'] = (df['TIME_OF_POSS'] * 60) / df['PACE']
df['Passes Per Second'] = df['PASSES_MADE'] / (df['TIME_OF_POSS'] * 60)
df = df[['TEAM_ID','TEAM_NAME','EFG_PCT','Seconds Per Possession','Passes Per Second']]

col = ["E13A3E","ED174C","002B5C","0F586C","002B5C","CE1141","007DC3","BAC3C9","724C9F","E03A3E","E56020","ED174C","00275D","007DC5","006BB6","061922","005083","00471B","98002E","FDB927","ED174C","CE1141","FDB927","4D90CD","007DC5","CE1141","B4975A","860038","008348","E13A3E"]

df = df.sort_values(by=['TEAM_ID'], ascending=False)
df['color'] = col

trace1 = go.Scatter(
    x=df['Seconds Per Possession'],
    y=df['Passes Per Second'],
    text=df['TEAM_NAME'],
    name="Team Passing",
    mode='markers',
    marker=dict(
        color=df['color'],
        size = df['EFG_PCT'],
        sizeref = .02
        )     
)

data = [trace1]
layout = go.Layout(
    title = "Passing",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Passing')