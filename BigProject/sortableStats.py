# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:46:03 2016

@author: pfenerty
"""
from dataGetters import getJson

class traditionalStats:
    def __init__(self,teamId,year,seasonType, measureType, tUrl):
        tradURL = tUrl.format(teamId=teamId, perMode="Totals", measureType=measureType, year=year, \
                                       seasonType=seasonType)
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
        advURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType="Advanced", year=year, seasonType=seasonType)
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
        ffURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType="Four+Factors", year=year, seasonType=seasonType)
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
        miscURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType="Misc", year=year, seasonType=seasonType)
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
        scoringURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType="Scoring", year=year, seasonType=seasonType)
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

class opponentStats(traditionalStats):
    def __init__(self,teamId,year,seasonType,measureType):
        super(opponentStats,self).__init__(self,teamId,year,seasonType,measureType)
        ffURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType="Four+Factors", year=year, seasonType=seasonType)
        data = getJson(ffURL,0)
        self.ftRate = data[12]
        self.tovPct = data[13]
        
    def __str__(self):
        return(super(opponentStats,self).__str__(self) + "\n" \
               "Free Throw Rate: " + str(self.ftRate) + "\n" \
               "Turover %: " +str(self.tovPct))
