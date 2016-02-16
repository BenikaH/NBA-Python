# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 13:40:13 2016

@author: pfenerty
"""

from json2pandas import json2pandas as j2p
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py

advURL = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
pace = j2p(advURL,0)
pace = pace[["TEAM_ID","TEAM_NAME","PACE","GP"]]
pace["dpt"] = 0

dURL = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID={team_id}&Outcome=&PORound=0&PerMode=Totals&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=Possessions&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
print("Getting Defensive Possession Time")
for index,team in pace.iterrows():
    print(team.TEAM_NAME)
    teamURL = dURL.format(team_id = team.TEAM_ID)
    tempDF = j2p(teamURL,0)
    dpt = tempDF['TIME_OF_POSS'].sum()
    pace.loc[index,'dpt'] = dpt
    
print("Getting Offensive Possession Time")
oURL = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=Totals&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=Possessions&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
tempDF = j2p(oURL,0)
tempDF = tempDF[["TEAM_ID","TIME_OF_POSS"]]
print("Merging")
pace = pd.merge(pace, tempDF, on=["TEAM_ID"], how="inner")
pace['otpp'] = pace['TIME_OF_POSS'] / ((pace['PACE'] / 48) * pace['GP'])
pace['dtpp'] = pace['dpt'] / ((pace['PACE'] / 48) * pace['GP'])

print("Graph me up Scotty")
trace0 = go.Scatter(
    x=pace['dtpp'],
    y=pace['otpp'],
    text=pace['TEAM_NAME'],
    mode='markers',
    marker=dict(
        size=pace['PACE'] - pace['PACE'].min(),
        sizeref = 0.2,
        color = pace['dtpp']-pace['otpp'],
        showscale = True,
    )
)
data = [trace0]
layout = go.Layout(
    showlegend=False,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='PaceChart')