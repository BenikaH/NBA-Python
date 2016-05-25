# -*- coding: utf-8 -*-
"""
Created on Thu May 19 07:49:36 2016

@author: pfenerty
"""

from dataGetters import j2p
import plotly.plotly as py
import plotly.graph_objs as go

basicUrl = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
hustleUrl = "http://stats.nba.com/stats/leaguehustlestatsplayer?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Playoffs&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

basicDf = j2p(basicUrl, 0)
hustleDf = j2p(hustleUrl, 0)

basicDf = basicDf[['PLAYER_ID','GP']]
hustleDf = hustleDf.merge(basicDf, on="PLAYER_ID", how="outer")

columns = ["CHARGES_DRAWN","CONTESTED_SHOTS","CONTESTED_SHOTS_2PT","CONTESTED_SHOTS_3PT","DEFLECTIONS","LOOSE_BALLS_RECOVERED","SCREEN_ASSISTS"]

for hustleStat in columns:
    temp = hustleDf.sort_values(by=hustleStat, ascending=False). head(20)
    
    x = temp['PLAYER_NAME']
    y = temp[hustleStat].astype(int)
    
    data = [
        go.Bar(
            x=x,
            y=y,
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5
                ),
            ),
            opacity=0.6
        )
    ]
    
    layout = go.Layout(
        title=hustleStat,
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='center',
                yanchor='bottom',
                showarrow=False,
            ) for xi, yi in zip(x, y)]
    )
    
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename="hustle/totals/"+hustleStat)
    
    
    temp[hustleStat] = temp[hustleStat]/temp["GP"]
    temp = temp.sort_values(by=hustleStat, ascending=False). head(20)
    
    x = temp['PLAYER_NAME']
    y = temp[hustleStat].round(decimals=2)    
    
    data = [
        go.Bar(
            x=x,
            y=y,
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5
                ),
            ),
            opacity=0.6
        )
    ]
    
    layout = go.Layout(
        title=hustleStat + "_PER_GAME",
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor='center',
                yanchor='bottom',
                showarrow=False,
            ) for xi, yi in zip(x, y)]
    )    
    
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename="hustle/perGame/"+hustleStat)