# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 09:36:16 2016

@author: pjfenert
"""

import pandas as pd
from json2pandas import json2pandas as j2p
    
synergy_url = "http://stats.nba.com/js/data/playtype/player_{play_type}.js"
play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup",\
            "OffRebound","PRRollMan","Spotup","Transition"]

averages = [0]*len(play_types)

synergy_df = pd.DataFrame()
for index,ptype in enumerate(play_types):
    url = synergy_url.format(play_type = ptype)
    temp_df = j2p(url,0)
    temp_df = temp_df[['PlayerIDSID','PlayerFirstName','PlayerLastName','PlayerNumber','P','TeamIDSID','TeamNameAbbreviation','GP','PPP','Points','Poss']]    
    temp_df.columns = ['PlayerID','PlayerFirstName','PlayerLastName','PlayerNumber','Position','TeamID','Team','GP',ptype+'_PPP',ptype+'_Points',ptype+'_Poss']    
    averages[index] = temp_df.sum(axis=0)[9]/float(temp_df.sum(axis=0)[10])     
    if index == 0:
        synergy_df = temp_df
    else:
        synergy_df = pd.merge(synergy_df,temp_df,on=["PlayerID","TeamID","GP","Position","PlayerFirstName","PlayerLastName","PlayerNumber","Team"],how="outer")
        
synergy_df.insert(8, 'Total_Poss', 0)
synergy_df.insert(9, 'Total_Points', 0)
synergy_df.insert(10, 'Total_PPP', 0)
synergy_df = synergy_df[:].fillna(0)

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

metrics_df = synergy_df.ix[:,0:11]
metrics_df['Offensive_Metric']=0
for index,player in synergy_df.iterrows():
    o_met = 0
    i=11
    for index2,ptype in enumerate(play_types):
        o_met += (player[i]-averages[index2])*player[i+2]
        i+=3
    metrics_df.loc[index,'Offensive_Metric'] = o_met
    
metrics_df.to_csv("offensive_metrics.csv")