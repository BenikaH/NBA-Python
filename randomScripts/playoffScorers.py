# -*- coding: utf-8 -*-
"""
Created on Tue May 03 18:56:24 2016

@author: fener
"""

from json2pandas import j2p
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py


url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

perGame = j2p(url, 0)
teamList = ['OKC','CLE','GSW','TOR']
perGame = perGame.loc[perGame['TEAM_ABBREVIATION'].isin(teamList)]
perGame = perGame.sort_values(['PTS'], ascending=False, axis=0)
perGame = perGame.head(15)

playerUrlTemplate = "http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID={playerId}&Season=2015-16&SeasonType=Playoffs"

traces = [go.Box()] * 15
i=0

for index,player in perGame.iterrows():
    playerUrl = playerUrlTemplate.format(playerId=player.PLAYER_ID)
    playerLog = j2p(playerUrl,0)
    pointList = playerLog['PTS'].tolist()
    traces[i] = go.Box(
        y = pointList,
        boxpoints = 'all',
        name = player.PLAYER_NAME
    )
    i+=1

plot_url = py.plot(traces, filename='playoffScorers')

