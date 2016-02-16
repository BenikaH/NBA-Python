# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 09:36:16 2016

@author: pjfenert
"""

import pandas as pd
from json2pandas import json2pandas as j2p
import plotly.plotly as py
import cufflinks as cf
import plotly.graph_objs as go
    
synergy_url = "http://stats.nba.com/js/data/playtype/player_{play_type}.js"
play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup",\
            "OffRebound","PRRollMan","Spotup","Transition"]

averages = [0]*len(play_types)

synergy_df = pd.DataFrame()
print("Getting Play Type Data")
for index,ptype in enumerate(play_types):
    print(ptype)
    url = synergy_url.format(play_type = ptype)
    temp_df = j2p(url,0)
    temp_df['PlayerName'] = temp_df['PlayerFirstName']+" "+temp_df['PlayerLastName']
    temp_df = temp_df[['PlayerIDSID','PlayerName','TeamIDSID','PPP','Points','Poss']]    
    temp_df.columns = ['PlayerID','PlayerName','TeamID',ptype+'_PPP',ptype+'_Points',ptype+'_Poss']    
    averages[index] = temp_df.sum(axis=0)[4]/float(temp_df.sum(axis=0)[5])     
    if index == 0:
        synergy_df = temp_df
    else:
        synergy_df = pd.merge(synergy_df,temp_df,on=["PlayerID","TeamID","PlayerName"],how="outer")
        
synergy_df.insert(3, 'Total_Poss', 0)
synergy_df.insert(4, 'Total_Points', 0)
synergy_df.insert(5, 'Total_PPP', 0)
synergy_df = synergy_df[:].fillna(0)

print("Calculating Totals")
for index,player in synergy_df.iterrows():
    synergy_df.loc[index,'Total_Poss'] = player.PRBallHandler_Poss+player.Cut_Poss+player.Handoff_Poss\
                                        +player.Isolation_Poss+player.Misc_Poss+player.OffScreen_Poss\
                                        +player.Postup_Poss+player.OffRebound_Poss+player.PRRollMan_Poss\
                                        +player.Spotup_Poss+player.Transition_Poss
    synergy_df.loc[index,'Total_Points'] = player.PRBallHandler_Points+player.Cut_Points+player.Handoff_Points\
                                        +player.Isolation_Points+player.Misc_Points+player.OffScreen_Points\
                                        +player.Postup_Points+player.OffRebound_Points+player.PRRollMan_Points\
                                        +player.Spotup_Points+player.Transition_Points
    synergy_df.loc[index,'Total_PPP'] = float(synergy_df.loc[index,'Total_Points']) / float(synergy_df.loc[index,'Total_Poss'])
    
synergy_df.to_csv("scoring_efficiency.csv")

metrics_df = synergy_df.ix[:,0:6]

for index,ptype in enumerate(play_types):
    metrics_df[ptype]=0

print('Calculating Offensive Metric')
metrics_df['Offensive_Metric']=0
for index,player in synergy_df.iterrows():
    o_met = 0
    i=6
    for index2,ptype in enumerate(play_types):
        o_met += (player[i]-averages[index2])*player[i+2]
        metrics_df.loc[index,ptype] = (player[i]-averages[index2])*player[i+1]
        i+=3
    metrics_df.loc[index,'Offensive_Metric'] = o_met
    
metrics_df.to_csv("offensive_metrics.csv")
metrics_df = metrics_df.sort_values(by=['Total_Poss'], ascending=False)

print('Adding advacned stats')
adv = j2p("http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight=",0)
adv['Total_Team_Poss'] = adv['GP']* adv['MIN'] * (adv['PACE']/48)
adv = adv[['PLAYER_ID','TEAM_ID','Total_Team_Poss','OFF_RATING']]
adv.columns = ['PlayerID','TeamID','Total_Team_Poss','ORtg']

adv = pd.merge(metrics_df.ix[:,0:6],adv,on=['PlayerID','TeamID'],how="inner")
adv['ScoringUsage'] = adv['Total_Poss'] / adv['Total_Team_Poss']

print('Adding position data')
positions = pd.read_csv("Position_Data.csv")
positions = positions[['Player','Pos.Est']]
positions.columns = ['PlayerName','Position']
for index,player in positions.iterrows():
    positions.loc[index,'Position'] = round(player.Position,0)
    
adv = pd.merge(adv,positions,on=['PlayerName'],how="inner")

col = ["E13A3E","ED174C","002B5C","0F586C","002B5C","CE1141","007DC3","BAC3C9","724C9F","E03A3E","E56020","ED174C","00275D","007DC5","006BB6","061922","005083","00471B","98002E","FDB927","ED174C","CE1141","FDB927","4D90CD","007DC5","CE1141","B4975A","860038","008348","E13A3E"]

teams = adv['TeamID'].unique()
teams.sort()
adv['color'] = 0
adv = adv.sort_values(by=['TeamID'], ascending=False)

teamid=0
i=-1
for index,player in adv.iterrows():
    if (teamid != (player.TeamID)):
        i+=1
    adv.loc[index,'color'] = col[i]
    teamid = player.TeamID

py_df = adv.sort_values(by=['ScoringUsage'], ascending = False)
py_df = py_df.head(150)

py1 = py_df.loc[py_df['Position'] == 1]
py2 = py_df.loc[py_df['Position'] == 2]
py3 = py_df.loc[py_df['Position'] == 3]
py4 = py_df.loc[py_df['Position'] == 4]
py5 = py_df.loc[py_df['Position'] == 5]

print("making da graf")
trace1 = go.Scatter(
    x=py1['ScoringUsage'],
    y=py1['Total_PPP'],
    text=py1['PlayerName'],
    name="Point Guards",
    mode='markers',
    marker=dict(
        color=py1['color'],
        size=py1['ORtg'] - py_df['ORtg'].min(),
        sizeref = 1,
    )
)
print("making da graf")
trace2 = go.Scatter(
    x=py2['ScoringUsage'],
    y=py2['Total_PPP'],
    text=py2['PlayerName'],
    name="Shooting Guards",
    mode='markers',
    marker=dict(
        color=py2['color'],
        size=py2['ORtg'] - py_df['ORtg'].min(),
        sizeref = 1,
    )
)
print("making da graf")
trace3 = go.Scatter(
    x=py3['ScoringUsage'],
    y=py3['Total_PPP'],
    text=py3['PlayerName'],
    name="Small Forwards",
    mode='markers',
    marker=dict(
        color=py3['color'],
        size=py3['ORtg'] - py_df['ORtg'].min(),
        sizeref = 1,
    )
)
print("making da graf")
trace4 = go.Scatter(
    x=py4['ScoringUsage'],
    y=py4['Total_PPP'],
    text=py4['PlayerName'],
    name="Power Forwards",
    mode='markers',
    marker=dict(
        color=py4['color'],
        size=py4['ORtg'] - py_df['ORtg'].min(),
        sizeref = 1,
    )
)
print("making da graf")
trace5 = go.Scatter(
    x=py5['ScoringUsage'],
    y=py5['Total_PPP'],
    text=py5['PlayerName'],
    name="Centers",
    mode='markers',
    marker=dict(
        color=py5['color'],
        size=py5['ORtg'] - py_df['ORtg'].min(),
        sizeref = 1,
    )
)


data = [trace1,trace2,trace3,trace4,trace5]
layout = go.Layout(
    title = "NBA SCORERS",
    showlegend=True,
    height=600,
    width=600,
)
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='scorers')













