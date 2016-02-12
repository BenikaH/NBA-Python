# -*- coding: utf-8 -*-
"""
Created on Sat Jan 09 15:42:00 2016

@author: Patrick
"""

import pandas as pd
import json
import urllib2
import plotly.plotly as py
import plotly.graph_objs as go
import time

def get_data_from_url(url,index):
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    data_dict = [dict(zip(headers, row)) for row in rows]
    return pd.DataFrame(data_dict)

teams_url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="    
teams_df = get_data_from_url(teams_url,0)
ORtg_df = pd.DataFrame(columns=teams_df['TEAM_NAME'].values.tolist())
DRtg_df = pd.DataFrame(columns=teams_df['TEAM_NAME'].values.tolist())
NRtg_df = pd.DataFrame(columns=teams_df['TEAM_NAME'].values.tolist())
max_games=0

for index,team in teams_df.iterrows():
    print(team.TEAM_NAME)    
    glog_url = "http://stats.nba.com/stats/teamgamelog?LeagueID=00&Season=2015-16&SeasonType=Regular+Season&TeamID={teamID}"
    glog_df = get_data_from_url(glog_url.format(teamID=team.TEAM_ID),0)
    print("got regular game log")
    game_url = "http://stats.nba.com/stats/boxscoreadvancedv2?EndPeriod=10&EndRange=28800&GameID={game_id}&RangeType=0&Season=2015-16&SeasonType=Regular+Season&StartPeriod=1&StartRange=0"    
    if len(glog_df)>max_games:
        max_games = len(glog_df)    
    adv_glog = [0]*max_games
    for index2,game in glog_df.iterrows():
        print("Game # " + str(index2))
        gid = game.Game_ID
        gdf = get_data_from_url(game_url.format(game_id=gid),1)
        adv_glog[index2] = [gdf.loc[0]['OFF_RATING'],gdf.loc[0]['OFF_RATING']-gdf.loc[0]['NET_RATING'],gdf.loc[0]['NET_RATING']]
    for i in range(len(glog_df),max_games):
        adv_glog[i] = [0,0,0]
    print("Got advanced game log")
    adv_glog_df = pd.DataFrame(adv_glog, columns={"Off_Rtg","Def_Rtg","Net_Rtg"})
    print("Made advanced game long DF")
    o_rtg_list = [0]*len(adv_glog)
    d_rtg_list = [0]*len(adv_glog)
    n_rtg_list = [0]*len(adv_glog)
    print("Made rating lists")
    for i in range(len(adv_glog)):
        o_rtg_list[i]=adv_glog[i][0]
        ORtg_df.loc[:][team.TEAM_NAME] = o_rtg_list
        d_rtg_list[i]=adv_glog[i][1]
        DRtg_df.loc[:][team.TEAM_NAME] = d_rtg_list
        n_rtg_list[i]=adv_glog[i][2]
        NRtg_df.loc[:][team.TEAM_NAME] = n_rtg_list
    print("Added team ratings to ratings data frames")
    time.sleep(500)
    

#data=[]
#for col in adv_glog_df.columns:
#    data.append(  go.Box( y=adv_glog_df[col], name=col, showlegend=False ) )
#
#data.append( go.Scatter( x = adv_glog_df.columns, y = adv_glog_df.mean(), mode='lines', name='mean' ) )
#
## IPython notebook
## py.iplot(data, filename='pandas-box-plot')
#
#url = py.plot(data, filename='pandas-box-plot')