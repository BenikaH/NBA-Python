# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 17:14:02 2016

@author: patirck
"""

from dataGetters import getJson,j2p
from url import url
from sortableStats import traditionalStats

class player:
    def __init__(self,playerId):
        self.seasonType = "Regular+Season"
        self.playerId = playerId
        pUrl = url.playInfo.format(playerId=playerId,seasonType=self.seasonType)
        data = getJson(pUrl,0)
        data=data[0]
        self.firstName = data[1]
        self.lastName = data[2]
        self.birthDate = data[6]
        self.college = data[7]
        self.country = data[8]
        self.height = data[10]
        self.weight = data[11]
        self.year = data[12]
        self.number = data[13]
        self.position = data[14]
        self.status = data[15]
        self.teamId = data[16]
        self.code = data[21]
        self.minYear = data[22]
        self.maxYear = data[23]
        self.dleague = data[24]
        self.gamesPlayed = data[25]
        #self.awards = j2p(url.playerAwards.format(playerId=playerId),0)
        
    def __str__(self):
        return("PlayerId: " + str(self.playerId) + "\n" \
               "Name: " + str(self.firstName) + " " + str(self.lastName) + "\n" \
               "Birthdate: " + str(self.birthDate) + "\n" \
               "College: " + str(self.college) + "\n" \
               "Country: " + str(self.country) + "\n" \
               "Height: " + str(self.height) + "\n" \
               "Weight: " + str(self.weight) + "\n" \
               "Experience: " + str(self.year) + "\n" \
               "Jersey Number: " + str(self.number) + "\n" \
               "Position: " + str(self.position) + "\n" \
               "Stats: " + str(self.status) + "\n" \
               "TeamId: " + str(self.teamId) + "\n" \
               "Code: " + str(self.code) + "\n" \
               "First Year: " + str(self.minYear) + "\n" \
               "Last Year: " + str(self.maxYear) + "\n" \
               "DLeague: " + str(self.dleague) + "\n" \
               "Played Game: " + str(self.gamesPlayed))
               
    def getTraditionalStats(self):
        self.traditional = traditionalStats(self.playerId,self.year,self.seasonType,"Totals",url.playerStats)
               