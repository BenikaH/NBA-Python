# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 15:38:16 2016

@author: pfenerty
"""

from dataGetters import j2p
import pandas as pd
import plotly.plotly as py
import cufflinks as cf

team_adv_url = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=" \
               "&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0" \
               "&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N" \
               "&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=" \
               "&StarterBench=&TeamID=0&VsConference=&VsDivision="
SVU_poss_url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=" \
               "&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0" \
               "&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=" \
               "&PtMeasureType=Possessions&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&StarterBench=" \
               "&TeamID=0&VsConference=&VsDivision=&Weight="

team_adv_df = j2p(team_adv_url, 0)
SVU_poss_df = j2p(SVU_poss_url, 0)

team_adv_df = team_adv_df[['TEAM_NAME', 'TEAM_ID', 'PACE', 'EFG_PCT', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']]
SVU_poss_df = SVU_poss_df[['TEAM_NAME', 'TEAM_ID', 'TIME_OF_POSS', 'TOUCHES']]
merged_df = pd.merge(team_adv_df, SVU_poss_df, on=['TEAM_NAME', 'TEAM_ID'], how="inner")
merged_df['TIME_PER_POSS'] = merged_df['TIME_OF_POSS'] / (merged_df['PACE']) * 60
merged_df['TOUCH_PER_SEC'] = merged_df['TOUCHES'] / (merged_df['TIME_OF_POSS'] * 60)
merged_df['TOUCH_PER_POSS'] = merged_df['TOUCHES'] / merged_df['PACE']
corr = merged_df.corr()

merged_df.iplot(kind='bubble', x='TIME_PER_POSS', y='TOUCH_PER_SEC', size='OFF_RATING', text='TEAM_NAME',
                xTitle='Seconds Per Possession', yTitle='Touches Per Possession',
                filename='PaceChart')
