# -*- coding: utf-8 -*-
"""
Created on Mon May 09 10:51:22 2016

@author: pfenerty
"""

import pandas as pd
from dataGetters import j2p
import difflib
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF

positionDf = pd.read_csv("Position_Data.csv")
positionDf = positionDf[['Player','Mins','Pos.Est','Team']]

reboundingUrl = "http://stats.nba.com/stats/leaguedashptstats?College=&" \
                "Conference=&Country=&DateFrom=&DateTo=&Division=&Draft" \
                "Pick=&DraftYear=&GameScope=&Height=&LastNGames=0&Leagu" \
                "eID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&POR" \
                "ound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=" \
                "Player&PlayerPosition=&PtMeasureType=Rebounding&Season" \
                "=2015-16&SeasonSegment=&SeasonType=Regular+Season&Star" \
                "terBench=&TeamID=0&VsConference=&VsDivision=&Weight="

reboundingDf = j2p(reboundingUrl, 0)
reboundingDf['Name_Match'] = reboundingDf['PLAYER_NAME'].apply(lambda x: difflib.get_close_matches(x, positionDf['Player']))

for index,player in reboundingDf.iterrows():
    if(len(player.Name_Match) == 0):
        reboundingDf.set_value(index,'Name_Match','thisStringShouldNotMatchAnything')
    else:
        reboundingDf.set_value(index,'Name_Match',player.Name_Match[0])


mergeDf = pd.merge(positionDf, reboundingDf, left_on='Player', 
                   right_on='Name_Match', how='inner')
                   
mergeDf = mergeDf[['Player','Mins','Pos.Est','Team','DREB','DREB_CHANCES','OREB','OREB_CHANCES','REB','REB_CHANCES']]

traces = [go.Scatter] * 6

mergeDf = mergeDf.sort_values(by=['REB_CHANCES'], ascending = False)

traces[0] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Player'],
    name = 'Guards',
    mode = 'markers'
)
traces[1] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Player'],
    name = 'Top 5 Guards',
    mode = 'markers'
)
traces[2] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Player'],
    name = 'Wings',
    mode = 'markers'
)
traces[3] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Player'],
    name = 'Top 5 Wings',
    mode = 'markers'
)
traces[4] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Player'],
    name = 'Bigs',
    mode = 'markers'
)
traces[5] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['REB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Player'],
    name = 'Top 5 Bigs',
    mode = 'markers'
)


layout = go.Layout(
    title='Position vs Rebound Chances',
    hovermode='closest',
    xaxis=dict(
        title='Player Position',
        zeroline=False,
    ),
    yaxis=dict(
        title='Rebound Chances',
    ),
)

fig = go.Figure(data=traces, layout=layout)
py.iplot(fig, filename='positionalRebounding/PositionVsRebChances')

traces = [go.Scatter] * 6

mergeDf = mergeDf.sort_values(by=['OREB_CHANCES'], ascending = False)

traces[0] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Player'],
    name = 'Guards',
    mode = 'markers'
)
traces[1] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Player'],
    name = 'Top 5 Guards',
    mode = 'markers'
)
traces[2] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Player'],
    name = 'Wings',
    mode = 'markers'
)
traces[3] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Player'],
    name = 'Top 5 Wings',
    mode = 'markers'
)
traces[4] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Player'],
    name = 'Bigs',
    mode = 'markers'
)
traces[5] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['OREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Player'],
    name = 'Top 5 Bigs',
    mode = 'markers'
)


layout = go.Layout(
    title='Position vs Offensive Rebound Chances',
    hovermode='closest',
    xaxis=dict(
        title='Player Position',
        zeroline=False,
    ),
    yaxis=dict(
        title='Rebound Chances',
    ),
)

fig = go.Figure(data=traces, layout=layout)
py.iplot(fig, filename='positionalRebounding/PositionVsORebChances')

traces = [go.Scatter] * 6

mergeDf = mergeDf.sort_values(by=['DREB_CHANCES'], ascending = False)

traces[0] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]['Player'],
    name = 'Guards',
    mode = 'markers'
)
traces[1] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] <= 2.5)].head(5)['Player'],
    name = 'Top 5 Guards',
    mode = 'markers'
)
traces[2] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]['Player'],
    name = 'Wings',
    mode = 'markers'
)
traces[3] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)].head(5)['Player'],
    name = 'Top 5 Wings',
    mode = 'markers'
)
traces[4] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)]['Player'],
    name = 'Bigs',
    mode = 'markers'
)
traces[5] = go.Scatter(
    x = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Pos.Est'],
    y = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['DREB_CHANCES'],
    text = mergeDf[(mergeDf['Pos.Est'] > 3.75)].head(5)['Player'],
    name = 'Top 5 Bigs',
    mode = 'markers'
)


layout = go.Layout(
    title='Position vs Defensive Rebound Chances',
    hovermode='closest',
    xaxis=dict(
        title='Player Position',
        zeroline=False,
    ),
    yaxis=dict(
        title='Rebound Chances',
    ),
)

fig = go.Figure(data=traces, layout=layout)
py.iplot(fig, filename='positionalRebounding/PositionVsDRebChances')




#guardsDf = mergeDf[(mergeDf['Pos.Est'] <= 2.5)]
#wingsDf = mergeDf[(mergeDf['Pos.Est'] > 2.5) & (mergeDf['Pos.Est'] <= 3.75)]
#bigsDf = mergeDf[(mergeDf['Pos.Est'] > 3.75)]
#
#teams = mergeDf['Team'].unique()
#
#teamRebDf = pd.DataFrame()
#teamRebDf['Team'] = teams
#teamRebDf['Guard_Oreb_Chances'] = 0
#teamRebDf['Wing_Oreb_Chances'] = 0
#teamRebDf['Big_Oreb_Chances'] = 0
#
#for index,team in teamRebDf.iterrows():
#    loopDf = guardsDf[guardsDf['Team'] == team.Team]
#    teamRebDf.set_value(index,'Guard_Oreb_Chances', loopDf['OREB_CHANCES'].sum())
#    loopDf = wingsDf[wingsDf['Team'] == team.Team]
#    teamRebDf.set_value(index,'Wing_Oreb_Chances', loopDf['OREB_CHANCES'].sum())
#    loopDf = bigsDf[bigsDf['Team'] == team.Team]
#    teamRebDf.set_value(index,'Big_Oreb_Chances', loopDf['OREB_CHANCES'].sum())
#    





























