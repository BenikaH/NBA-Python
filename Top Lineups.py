# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 07:31:54 2016

@author: pfenerty
"""

from json2pandas import json2pandas as j2p
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
teams = j2p(url,0)
teams = teams[['TEAM_ID','TEAM_NAME']]

url = "http://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity={group_quant}&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID=0&VsConference=&VsDivision="
for i in range(2,5):
    print(str(i) + ' MAN GROUPS')
    topDF = pd.DataFrame(columns = ['GROUP_ID','GROUP_NAME','TEAM_ABBREVIATION','TEAM_NAME','MIN','OFF_RATING','DEF_RATING'])    
    tempURL = url.format(group_quant=i)
    groupsDF = j2p(tempURL,0)
    groupsDF = groupsDF[['GROUP_ID','GROUP_NAME','TEAM_ABBREVIATION','TEAM_ID','MIN','OFF_RATING','DEF_RATING']]
    groupsDF = groupsDF.sort_values(by='MIN', ascending=False)
    for index,team in teams.iterrows():
        print(team.TEAM_NAME)
        teamID = team.TEAM_ID
        tempDF = groupsDF.loc[groupsDF['TEAM_ID']==teamID]
        tempDF = tempDF.sort_values(by='MIN', ascending = False)
        tempDF = tempDF.head(10)                
        tempDF = tempDF.sort_values(by='OFF_RATING', ascending = False)        
        tempDF = tempDF.head(1)
        topDF = topDF.append(tempDF, ignore_index=True)
    topDF = topDF.sort_values(by='OFF_RATING', ascending = False)
    print('Plotting')
    trace0 = go.Bar(
        x = topDF['TEAM_ABBREVIATION'],
        y = topDF['OFF_RATING'],
        text = topDF['GROUP_NAME'],
        visible = True,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )
    data = [trace0]
    layout = go.Layout(
        title='Top ' + str(i) + ' Man Groups',
    )
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='TopLineups/Top ' + str(i) + ' Man Groups')
    topDF.to_csv("Top " + str(i) + " Man Groups")
        
        

