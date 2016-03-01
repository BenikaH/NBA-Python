# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 08:17:12 2016

@author: pfenerty
"""

import pandas as pd
import json
import urllib2

def j2p(url,index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    headers = data['resultSets'][index]['headers']
    rows = data['resultSets'][index]['rowSet']
    data_dict = [dict(zip(headers, row)) for row in rows]
    return pd.DataFrame(data_dict)
    
def getJson(url,index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = json.loads(response.read())
    data = data['resultSets'][index]['rowSet']
    return data

class url:
    teamInfo = "http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType={seasonType}&TeamID={teamId} \
                &season={year}"
    teamRoster = "http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season={year}&TeamID={teamId}"
    teamStats = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope= \
                &GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType={measureType}&Month=0&OpponentTeamID= \
                0&Outcome=&PORound=0&PaceAdjust=N&PerMode={perMode}&Period=0&PlayerExperience=&PlayerPosition=&Plu \
                sMinus=N&Rank=N&Season={year}&SeasonSegment=&SeasonType={seasonType}&ShotClockRange=&StarterBench= \
                &TeamID={teamId}&VsConference=&VsDivision="
    #teamId is a 10 digit unique identifier
    #year is in the format 2015-16
    #seasonType => [Regular+Season,Pre+Season,Playoffs,All-Star]
    #perMode => [PerGame,Per100Possessions,Totals,Per100Plays,Per48,Per36,Per30,PerMinute,PerPossession,PerPlay,MinutesPer]

class paramEnums:
    seasonTypes = ["Regular+Season","Pre+Season","Playoffs","All-Star"]
    perModes = ["PerGame","Per100Possessions","Totals","Per100Plays","Per48","Per36","Per30","PerMinute","PerPossession","PerPlay,MinutesPer"]     
    measureTypes = ["Base","Advanced","Misc"]    
    
class traditionalStats:
    def __init__(self,teamId,year,seasonType):
        tradURL = url.teamStatsTrad.format(teamId=teamId, perMode="Totals", measureType="Base", year=year, seasonType=seasonType)
        data = getJson(tradURL,0)
        data = data[0]
        self.min = data[6]
        self.gp = data[2]
        self.fgm = data[7]
        self.fga = data[8]
        self.fg3m = data[10]
        self.fg3a = data[11]
        self.ftm = data[13]
        self.fta = data[14]
        self.oreb = data[16]
        self.dreb = data[17]
        self.ast = data[19]
        self.tov = data[20]
        self.stl = data[21]
        self.blk = data[22]
        self.blka = data[23]
        self.pf = data[24]
        self.pfd = data[25]
        self.pts = data[26]
        self.plusMinus = data[27]
        
    def __str__(self):
        return("Minutes: " + str(self.min) + "\n" \
               "Games Played:" + str(self.gp) + "\n" \
               "Field Goals Made: " + str(self.fgm) + "\n" \
               "Field Goals Attempted: " + str(self.fga) + "\n" \
               "3pt Field Goals Made: " + str(self.fg3m) + "\n" \
               "3pt Field Goals Attempted: " + str(self.fg3a) + "\n"
               "Free Throws Made: " + str(self.ftm) + "\n" \
               "Free Throws Attemped: " + str(self.fta) + "\n" \
               "Offensive Rebounds: " + str(self.oreb) + "\n" \
               "Defensive Rebounds: " + str(self.dreb) + "\n" \
               "Assists: " + str(self.ast) + "\n" \
               "Turnovers: " + str(self.tov) + "\n" \
               "Steals: " + str(self.stl) + "\n" \
               "Blocks: " + str(self.blk) + "\n" \
               "Attempts Blocked " + str(self.blka) + "\n" \
               "Personal Fouls: " + str(self.pf) + "\n" \
               "Personal Fouls Drawn: " + str(self.pfd) + "\n" \
               "Points: " + str(self.pts) + "\n" \
               "Plus/Minus: " + str(self.plusMinus) + "\n")
    
    def fgPct(self):
        return float(self.fgm/self.fga)
        
    def fg2Pct(self):
        return float((self.fgm-self.fg3m)/(self.fga-self.fg3a))
    
    def fg3Pct(self):
        return float(self.fg3m/self.fg3a)
        
    def ftPct(self):
        return float(self.ftm/self.fta)
        
    def efgPct(self):
        return float((self.fgm+(0.5*self.fg3m)/self.fga))
        
    def tsPct(self):
        return float(self.pts/(2*(self.fga+(0.44*self.fta))))

class advancedStats:
    def __init__(self,teamId,year,seasonType):     
        advURL = url.teamStatsTrad.format(teamId=teamId, perMode="Totals", measureType="Advanced", year=year, seasonType=seasonType)
        data = getJson(advURL,0)[0]
        self.ortg = data[7]
        self.drtg = data[8]
        self.astPct = data[10]
        self.astTov = data[11]
        self.astRatio = data[12]
        self.orebPct = data[13]
        self.drebPct = data[14]
        self.rebPct = data[15]
        self.tovPct = data[16]
        self.pace = data[19]
        ffURL = url.teamStatsTrad.format(teamId=teamId, perMode="Totals", measureType="Four+Factors", year=year, seasonType=seasonType)
        data = getJson(ffURL,0)
        self.ftRate = data[8]
        
    def __str__(self):
        return("Offensive Rating: " + str(self.ortg) + "\n" \
               "Defensive Rating: " + str(self.drtg) + "\n" \
               "Assist %: " + str(self.astPct) + "\n" \
               "Assist To Turnover Ratio: " + str(self.astTov) + "\n" \
               "Assists Ration: " + str(self.astRatio) + "\n" \
               "Offensive Rebound %: " + str(self.orebPct) + "\n" \
               "Defensive Rebound %: " + str(self.drebPct) + "\n" \
               "Total Rebound %: " + str(self.rebPct) + "\n" \
               "Turnover %: " + str(self.tovPct) + "\n" \
               "Free Throw Rate: " + str(self.ftRate) + "\n" \
               "Pace: " + str(self.pace))

class miscStats:
    def __init__(self,teamId,year,seasonType):     
        miscURL = url.teamStatsTrad.format(teamId=teamId, perMode="Totals", measureType="Misc", year=year, seasonType=seasonType)
        data = getJson(miscURL,0)[0]
        self.ptsOffTov = data[7]
        self.pts2ndChance = data[8]
        self.ptsFastBreak = data[9]
        self.ptsPaint = data[10]
        
    def __str__(self):
        return("Points Off Turovers: " + str(self.ptsOffTov) + "\n" \
               "Second Change Points: " + str(self.pts2ndChance) + "\n" \
               "Fast Break Points: " + str(self.ptsFastBreak) + "\n" \
               "Points in the Paint: " + str(self.ptsPaint))

class scoringStats:
    def __init__(self,teamId,year,seasonType):     
        scoringURL = url.teamStatsTrad.format(teamId=teamId, perMode="Totals", measureType="Scoring", year=year, seasonType=seasonType)
        data = getJson(scoringURL,0)[0]
        self.pctFga2 = data[7]
        self.pctFga3 = data[8]
        self.pctPts2 = data[9]
        self.pctPtsMR = data[10]
        self.pctPts3= data[11]
        self.pctPtsFB = data[12]
        self.pctPtsFT = data[13]
        self.pctPtsOffTov = data[14]
        self.pctPtsPaint = data[15]
        self.pctAst2 = data[16]
        self.pctAst3 = data[18]
        self.pctAst = data[20]
        
    def __str__(self):
        return("Percentage of Field Goals which are 2s: " + str(self.pctFga2) + "\n" \
               "Percentage of Field Goals which are 3s: " + str(self.pctFga3) + "\n" \
               "Percentage of Points from 2s: " + str(self.pctPts2) + "\n" \
               "Percentage of Points from Mid Range: " + str(self.pctPtsMR) + "\n" \
               "Percentage of Points from 3s: " + str(self.pctPts3) + "\n" \
               "Precentage of Points from Fast Breaks: " + str(self.pctPtsFB) + "\n" \
               "Percentage of Points from Free Throws: " + str(self.pctPtsFT) + "\n" \
               "Percentage of Points off Turnovers: " + str(self.pctPtsOffTov) + "\n" \
               "Percentage of Points in the Paint: " + str(self.pctPtsPaint) + "\n" \
               "Percentage of 2s Assisted: " + str(self.pctAst2) + "\n" \
               "Percentage of 3s Assisted: " + str(self.pctAst3) + "\n" \
               "Percentage of All Shots Assisted: " + str(self.pctAst))
    

class team:   
    def __init__(self,teamId,seasonType,year):
        data = getJson(url.teamInfo.format(teamId=teamId, seasonType=seasonType, year=year),0)
        data = data[0]
        self.teamId = data[0]
        self.year = data[1]
        self.seasonType = seasonType
        self.city = data[2]
        self.abb = data[3]
        self.conf = data[4]
        self.div = data[5]
        self.code = data[6]
        self.wins = data[7]
        self.losses = data[8]
        self.winPct = data[9]
        self.confRank = data[10]
        self.divRank = data[11]
        self.minYear = data[12]
        self.maxYear = data[13]
        self.roster = j2p(url.teamRoster.format(teamId=teamId, seasonType=seasonType, year=year),0)
        self.coaches = j2p(url.teamRoster.format(teamId=teamId, seasonType=seasonType, year=year),1)
        
    def __str__(self):
        return("Team Id: " + str(self.teamId) + "\n" \
               "Year: " + str(self.year) + "\n" \
               "Season Type: " + str(self.seasonType) + "\n" \
               "City: " + str(self.city) + "\n" \
               "Abbreviation: " + str(self.abb) + "\n" \
               "Conference: " + str(self.conf) + "\n" \
               "Division: " + str(self.div) + "\n" \
               "Code: " + str(self.code) + "\n" \
               "Wins: " + str(self.wins) + "\n" \
               "Losses: " + str(self.losses) + "\n" \
               "Win %: " + str(self.winPct) + "\n" \
               "Conference Standing: " + str(self.confRank) + "\n" \
               "Division Standing: " + str(self.divRank) + "\n" \
               "First Year: " + str(self.minYear) + "\n" \
               "Last Year: " + str(self.maxYear) + "\n" \
               "Roster: " + str(self.roster) + "\n" \
               "Coaches: " + str(self.coaches))
        
    def getTraditionalStats(self):
        self.traditional = traditionalStats(self.teamId, self.year, self.seasonType)
        
    def getAdvancedStats(self):
        self.advanced = advancedStats(self.teamId, self.year, self.seasonType)
        
    def getMiscStats(self):
        self.misc = miscStats(self.teamId, self.year, self.seasonType)
        
    
    
hawks = team('1610612737','Regular+Season','2015-16')    