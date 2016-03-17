# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 19:06:33 2016

@author: patrick
"""

from dataGetters import j2p
import pandas as pd

playerStatsUrl = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
playerStats = j2p(playerStatsUrl,0)
playerStats = playerStats.loc[playerStats['MIN']>=25]
playerStats = playerStats.loc[playerStats['GP']>=40]
playerStats = playerStats[['TEAM_ID','PLAYER_ID','PIE','MIN','PLAYER_NAME']]

teams = playerStats['TEAM_ID'].unique()

df = pd.DataFrame(columns=['PlayerId1','PlyaerName1','PlayerId2','PlayerName2','TotalIndvMins'])

for teamId in teams:
     teamStats = playerStats.loc[playerStats['TEAM_ID']==teamId]
     teamStats = teamStats.sort_values(by=['PIE'],ascending=False)
     teamStats = teamStats.head(2)
     playerIds = teamStats['PLAYER_ID'].unique()
     playerIds.sort()
     mins = teamStats['MIN'].unique()
     names = teamStats['PLAYER_NAME'].unique()
     teamRow = [playerIds[0],names[0],playerIds[1],names[1],(mins[0]+mins[1])]
     df=df.append(pd.Series(teamRow,index=df.columns),ignore_index=True)

lineUps = pd.DataFrame()
for teamId in teams:
     teamLineUpsUrl = "http://stats.nba.com/stats/teamdashlineups?DateFrom=&DateTo=&GameID=&GameSegment=&GroupQuantity=2&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID={teamId}&VsConference=&VsDivision="
     teamLineUpsUrl = teamLineUpsUrl.format(teamId = teamId)
     teamLineUps = j2p(teamLineUpsUrl,1)
     lineUps = lineUps.append(teamLineUps,ignore_index=True)
     
     
#lineUpsUrl = "http://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=2&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID=0&VsConference=&VsDivision="
#lineUpStats = j2p(lineUpsUrl,0)
#lineUpStats = lineUpStats[['GROUP_ID','GROUP_NAME','MIN']]
lineUps['PlayerId1'] = 0
lineUps['PlayerId2'] = 0
#
for index, lineUp in lineUps.iterrows():
    temp = lineUp.GROUP_ID.split('-')
    temp.sort()    
    lineUps.ix[index,'PlayerId1'] = float(temp[0])
    lineUps.ix[index,'PlayerId2'] = float(temp[1])

lineUps = lineUps[['PlayerId1','PlayerId2','MIN','GROUP_NAME']]    

merge = pd.DataFrame(columns=['PlayerId1','PlayerId2','TotalIndvMins','MinsTogether','PlayerNames'])

merge1 = df.merge(lineUps,left_on=['PlayerId1','PlayerId2'],right_on=['PlayerId1','PlayerId2'],how='inner')
merge2 = df.merge(lineUps,left_on=['PlayerId1','PlayerId2'],right_on=['PlayerId2','PlayerId1'],how='inner')
merge = merge1.append(merge2,ignore_index=True)

merge.to_csv('staggering.csv')