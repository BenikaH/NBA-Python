# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:51:54 2016

@author: pfenerty
"""
from url import url
from dataGetters import getJson


class synergy():
    def __init__(self,playerOrTeam,playType,teamId):
        synUrl = url.synergy.format(playerOrTeam=playerOrTeam,playType=playType,teamId=teamId)
        print(synUrl)
        data = getJson(synUrl,0)
        for i in range(len(data)):
            if teamId==data[i][0]:
                data=data[i]
                break
        self.poss = data[5]
        self.freq = data[6]
        self.points = data[7]
        self.fga = data[8]
        self.fgm = data[9]
        self.ppp = data[10]
        self.perc = data[11]/(data[11]+data[12])
        self.efg = data[20]
        self.ftPct = data[21]
        self.toPct = data[22]
        self.sf = data[23]
        self.andOne = data[24]
        self.scorePct = data[25]
        
    def __str__(self):
        return("Possessions: " + str(self.poss) + "\n" \
               "Frequency: " + str(self.freq) + "\n" \
               "Points: " + str(self.points) + "\n" \
               "Feild Goal Attempts: " + str(self.fga) + "\n" \
               "Field Goal Makes: " + str(self.fgm) + "\n" \
               "Points Per Play: " + str(self.ppp) + "\n" \
               "Percentile: " + str(self.perc) + "\n" \
               "Effective FG%: " + str(self.efg) + "\n" \
               "FT Freq: " + str(self.ftPct) + "\n" \
               "Turnover Freq: " + str(self.toPct) + "\n" \
               "Shooting Foul Freq: " + str(self.sf) + "\n" \
               "And One Freq: " + str(self.andOne) + "\n" \
               "Score Freq: " + str(self.scorePct))