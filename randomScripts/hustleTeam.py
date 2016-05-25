# -*- coding: utf-8 -*-
"""
Created on Thu May 19 10:25:32 2016

@author: pfenerty
"""

from dataGetters import j2p
import pandas as pd

gameLogUrl = "http://stats.nba.com/stats/leaguegamelog?Counter=1000&Direction=DESC&LeagueID=00&PlayerOrTeam=T&Season=2015-16&SeasonType=Playoffs&Sorter=PTS"
advBoxUrl = "http://stats.nba.com/stats/boxscoreadvancedv2?EndPeriod=10&EndRange=31800&GameID={gameId}&RangeType=0&Season=2015-16&SeasonType=Playoffs&StartPeriod=1&StartRange=0"
tradBoxUrl = "http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=31800&GameID={gameId}&RangeType=0&Season=2015-16&SeasonType=Playoffs&StartPeriod=1&StartRange=0"
hustleBoxUrl = "http://stats.nba.com/stats/hustlestatsboxscore?GameID={gameId}"

gameLogDf = j2p(gameLogUrl, 0)
games = gameLogDf.ix[:,13]

df = pd.DataFrame()

for game in games:
    advUrl = advBoxUrl.format(gameId=game)
    tradUrl = tradBoxUrl.format(gameId=game)
    hustleUrl = hustleBoxUrl.format(gameId=game)
    advGameDf = j2p(advUrl, 1)
    advGameDf = advGameDf[['TEAM_ID','PACE','NET_RATING','OFF_RATING']]
    advGameDf['DEF_RATING'] = advGameDf['OFF_RATING'] - advGameDf['NET_RATING']
    tradGameDf = j2p(tradUrl, 1)
    tradGameDf = tradGameDf[['TEAM_ID','FGA','TO']]
    hustleGameDf = j2p(hustleUrl, 2)
    temp = pd.merge(advGameDf, hustleGameDf, on="TEAM_ID", how="inner")
    temp = temp.merge(tradGameDf, on="TEAM_ID", how="inner")
    df = df.append(temp, ignore_index=False)
    2+2