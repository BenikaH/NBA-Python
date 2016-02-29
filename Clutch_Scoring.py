# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 10:11:59 2016

@author: pfenerty
"""

from json2pandas import json2pandas as j2p
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

url_template = "http://stats.nba.com/stats/leaguedashplayerclutch?AheadBehind=Behind+or+Tied&ClutchTime=Last+30+Seconds&College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&PointDiff=4&Rank=N&Season={year}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
year1 = 1996
year2 = year1 + 1
year = str(year1) + "-" + str(year2)[2:4]

clutch_df = pd.DataFrame(columns = ['PLAYER_ID','PLAYER_NAME','FGM','FGA','FG3M','FG3A'])
while year1 < 2016:
    print(year)
    url = url_template.format(year=year)
    year_df = j2p(url,0)
    year_df = year_df[['PLAYER_ID','PLAYER_NAME','FGM','FGA','FG3M','FG3A']]
    temp = pd.merge(year_df,clutch_df,on=['PLAYER_ID','PLAYER_NAME'], how="outer")
    temp = temp.fillna(0)
    if year1 == 1996:
        clutch_df = temp
    else:
        temp['FGA'] = temp['FGA_x'] + temp['FGA_y']
        temp['FGM'] = temp['FGM_x'] + temp['FGM_y']
        temp['FG3A'] = temp['FG3A_x'] + temp['FG3A_y']
        temp['FG3M'] = temp['FG3M_x'] + temp['FG3M_y']
        temp=temp[['PLAYER_ID','PLAYER_NAME','FGM','FGA','FG3M','FG3A']]
        clutch_df=clutch_df[['PLAYER_ID','PLAYER_NAME']]
        clutch_df = pd.merge(clutch_df,temp,on=['PLAYER_ID','PLAYER_NAME'], how="outer")
    year1+=1
    year2+=1
    year = str(year1) + "-" + str(year2)[2:4]
    
clutch_df['EFG'] = (clutch_df["FGM"] + 0.5*clutch_df["FG3M"])/clutch_df["FGA"]

fifty = clutch_df.loc[clutch_df['FGA']>=50]
forty = clutch_df.loc[clutch_df['FGA']>=40]
thirty = clutch_df.loc[clutch_df['FGA']>=30]
twenty = clutch_df.loc[clutch_df['FGA']>=20]
ten = clutch_df.loc[clutch_df['FGA']>=10]

trace1 = go.Scatter(
    x=fifty['FGA'],
    y=fifty['EFG'],
    text=fifty['PLAYER_NAME'],
    name="More than 50 shots",
    mode='markers',
)
trace2 = go.Scatter(
    x=forty['FGA'],
    y=forty['EFG'],
    text=forty['PLAYER_NAME'],
    name="More than 40 shots",
    mode='markers',
)
trace3 = go.Scatter(
    x=thirty['FGA'],
    y=thirty['EFG'],
    text=thirty['PLAYER_NAME'],
    name="More than 30 shots",
    mode='markers',
)
trace4 = go.Scatter(
    x=twenty['FGA'],
    y=twenty['EFG'],
    text=twenty['PLAYER_NAME'],
    name="More than 20 shots",
    mode='markers',
)
trace5 = go.Scatter(
    x=ten['FGA'],
    y=ten['EFG'],
    text=ten['PLAYER_NAME'],
    name="More than 10 shots",
    mode='markers',
)

data = [trace1,trace2,trace3,trace4,trace5]
layout = go.Layout(
    title = "Clutch Scoring",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='Clutch Scoring 2')