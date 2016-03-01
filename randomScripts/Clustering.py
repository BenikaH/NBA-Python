# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 13:37:10 2016

@author: pfenerty
"""

from json2pandas import json2pandas as j2p
import pandas as pd
import plotly.plotly as py
import cufflinks as cf

totals = j2p("http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=",0)
totals = totals.loc[totals['FGM']>=300]
totals = totals[['PLAYER_ID','PLAYER_NAME','TEAM_ID','FGA','FGM','FG3A','FG3M','FTA','FTM']]
totals['2P%'] = (totals['FGM'] - totals['FG3M']) / (totals['FGA'] / totals['FG3A'])
totals['3P%'] = totals['FG3M'] / totals['FG3A']
totals['FT%'] = totals['FTM'] / totals['FTA']
df = totals[['PLAYER_NAME','2P%','3P%','FT%']]
#per100 = j2p("http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per100Possessions&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=",0)
#df = pd.merge(totals,per100,on=['PLAYER_ID','TEAM_ID'], how="inner")
#df = df[['PLAYER_ID','TEAM_ID','PTS','AST','REB']]


scatter = dict(
    mode = "markers",
    name = "y",
    type = "scatter3d",    
    x = df['2P%'], y = df['3P%'], z = df['FT%'],
    text=df['PLAYER_NAME'],
    marker = dict( size=2, color="rgb(23, 190, 207)")
)
clusters = dict(
    alphahull = -1,
    name = "y",
    opacity = 0.1,
    type = "mesh3d",    
    x = df['2P%'], y = df['3P%'], z = df['FT%']
)
layout = dict(
    title = '3d point clustering',
    scene = dict(
        xaxis = dict( zeroline=False ),
        yaxis = dict( zeroline=False ),
        zaxis = dict( zeroline=False ),
    )
)
fig = dict( data=[scatter, clusters], layout=layout )
# Use py.iplot() for IPython notebook
url = py.plot(fig, filename='3d point clustering')