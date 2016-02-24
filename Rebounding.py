# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:30:13 2016

@author: pfenerty
"""

import pandas as pd
from json2pandas import json2pandas as j2p
import plotly.plotly as py
import cufflinks as cf
import plotly.graph_objs as go

url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Player&PlayerPosition=&PtMeasureType=Rebounding&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
reb = j2p(url,0)
reb = reb.sort_values(by="REB_CHANCES",ascending=False)
reb = reb.head(30)

col = ["E13A3E","ED174C","002B5C","0F586C","002B5C","CE1141","007DC3","BAC3C9","724C9F","E03A3E","E56020","ED174C","00275D","007DC5","006BB6","061922","005083","00471B","98002E","FDB927","ED174C","CE1141","FDB927","4D90CD","007DC5","CE1141","B4975A","860038","008348","E13A3E"]

teams = reb['TEAM_ID'].unique()
teams.sort()
reb['color'] = 0
reb = reb.sort_values(by=['TEAM_ID'], ascending=False)

teamid=0
i=-1
for index,player in reb.iterrows():
    if (teamid != (player.TEAM_ID)):
        i+=1
    reb.loc[index,'color'] = col[i]
    teamid = player.TEAM_ID

trace1 = go.Scatter(
    x=reb['REB_CONTEST'],
    y=reb['REB_UNCONTEST'],
    text=reb['PLAYER_NAME'],
    name="Rebounders",
    mode='markers',
    marker=dict(
        color=reb['color'],
        size=reb['REB'] - reb['REB'].min() + 1,
        sizeref = 0.3,
    )
)

data = [trace1]
layout = go.Layout(
    title = "Uncontested vs Contested Rebounds",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='rebounding/contest')

trace2 = go.Scatter(
    x=reb['REB_CHANCES'],
    y=reb['REB_CHANCE_PCT'],
    text=reb['PLAYER_NAME'],
    name="Rebounders",
    mode='markers',
    marker=dict(
        size=reb['REB'] - reb['REB'].min() + 1,
        color=reb['color'],
        sizeref=0.3,
    )
)

data = [trace2]
layout = go.Layout(
    title = "Rebound Chances vs Rebound Percentage",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='rebounding/pct')

trace3 = go.Scatter(
    x=reb['OREB'],
    y=reb['DREB'],
    text=reb['PLAYER_NAME'],
    name="Rebounders",
    mode='markers',
    marker=dict(
        size=reb['REB'] - reb['REB'].min() + 1,
        color=reb['color'],
        sizeref = 0.3,
    )
)

data = [trace3]
layout = go.Layout(
    title = "Offensive vs Defensive Rebounds",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='rebounding/OvsD')