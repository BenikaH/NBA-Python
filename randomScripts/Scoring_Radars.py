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
    
synergy_df = synergy_df.sort_values(by=['Total_Points'], ascending=False)

print("Making Charts")
i=0
for index,player in synergy_df.iterrows():    
    if i > 5:
        break
    i += 1
    print("Making Chart for: " + player.PlayerName)
    points = [0] * 11
    efficiency = [0] * 11
    j=0
    for index2,pt in enumerate(play_types):
        points[j] = synergy_df.loc[index,pt+'_Points']
        efficiency[j] = synergy_df.loc[index,pt+'_PPP']
        j+=1
        
    trace1 = go.Area(
    r=points,
    t=play_types,
    name=player.PlayerName,
    marker=dict(
        color=synergy_df.loc[index,'Total_PPP']
        )
    )

    layout = go.Layout(
        title='Wind Speed Distribution in Laurel, NE',
        font=dict(
            size=16
            ),
        legend=dict(
            font=dict(
                size=16
            )
        ),
        radialaxis=dict(
            showticklabels=True,
            ticksuffix='%'
        ),
        orientation=0
    )
    
    data = [trace1]    
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='/synergy_charts' + player.PlayerName + ' Synergy-chart')
        


#synergy_df.to_csv("scoring_efficiency.csv")
#
#metrics_df = synergy_df.ix[:,0:6]
#
#for index,ptype in enumerate(play_types):
#    metrics_df[ptype]=0
#
#print('Calculating Offensive Metric')
#metrics_df['Offensive_Metric']=0
#for index,player in synergy_df.iterrows():
#    o_met = 0
#    i=6
#    for index2,ptype in enumerate(play_types):
#        o_met += (player[i]-averages[index2])*player[i+2]
#        metrics_df.loc[index,ptype] = (player[i]-averages[index2])*player[i+1]
#        i+=3
#    metrics_df.loc[index,'Offensive_Metric'] = o_met
#    
#metrics_df.to_csv("offensive_metrics.csv")
#metrics_df = metrics_df.sort_values(by=['Total_Poss'], ascending=False)

