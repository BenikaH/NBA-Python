# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 08:17:12 2016

@author: pfenerty
"""

from url import url
from sortableStats import traditionalStats,advancedStats,miscStats,scoringStats,opponentStats
from dataGetters import j2p,getJson
from synergy import synergy
from sportsVU import svuCatchAndShoot,svuDrives,svuDefense,svuPassing,svuPullUpShooting,svuRebounding \
                    ,svuMovement,svuTouchLocation,svuPossession
    
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
        tUrl = url.teamStats
        self.traditional = traditionalStats(self.teamId, self.year, self.seasonType, "Base", tUrl)
        
    def getAdvancedStats(self):
        self.advanced = advancedStats(self.teamId, self.year, self.seasonType)
        
    def getMiscellaneousStats(self):
        self.misc = miscStats(self.teamId, self.year, self.seasonType)
        
    def getScoringStats(self):
        self.scoring = scoringStats(self.teamId, self.year, self.seasonType)
    
    def getOpponentStats(self):
        self.opponent = opponentStats(self.teamId, self.year, self.seasonType, "Opponent")
        
    def getAllSortableStats(self):
        self.getTraditionalStats()
        self.getAdvancedStats()
        self.getMiscellaneousStats()
        self.getScoringStats()
        self.getOpponentStats()
    
#   play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup","OffRebound","PRRollMan","Spotup","Transition"]
    def getBallHandlerStats(self):
        self.ballHandler = synergy("team","PRBallHandler",self.teamId)
        
    def getCutStats(self):
        self.cut = synergy("team","Cut",self.teamId)
    
    def getHandOffStats(self):
        self.handOff = synergy("team","Handoff",self.teamId)
        
    def getIsoStats(self):
        self.iso = synergy("team","Isolation",self.teamId)
        
    def getMiscStats(self):
        self.misc = synergy("team","Misc",self.teamId)
        
    def getScreenStats(self):
        self.screen = synergy("team","OffScreen",self.teamId)
        
    def getPostUpStats(self):
        self.postUp = synergy("team","Postup",self.teamId)
        
    def getOffReboundStats(self):
        self.offReb = synergy("team","OffRebound",self.teamId)

    def getRollManStats(self):
        self.rollMan = synergy("team","PRRollMan",self.teamId)
        
    def getSpotUpStats(self):
        self.spotUp = synergy("team","Spotup",self.teamId)
        
    def getTransitionStats(self):
        self.transition = synergy("team", "Transition", self.teamId)
        
    def getAllSynergyStats(self):
        self.getBallHandlerStats()
        self.getCutStats()
        self.getHandOffStats()
        self.getIsoStats()
        self.getMiscStats()
        self.getScreenStats()
        self.getPostUpStats()
        self.getOffReboundStats()
        self.getRollManStats()
        self.getSpotUpStats()
        self.getTransitionStats()
        
    def getCatchAndShootStats(self):
        self.catchAndShoot = svuCatchAndShoot("Totals",self.year,self.seasonType,self.teamId)
        
    def getDriveStats(self):
        self.drives = svuDrives("Totals",self.year,self.seasonType,self.teamId)
        
    def getRimProtectionStats(self):
        self.rimProtect = svuDefense("Totals",self.year,self.seasonType,self.teamId)
        
    def getPassingStats(self):
        self.passing = svuPassing("Totals",self.year,self.seasonType,self.teamId)
        
    def getPossessionStats(self):
        self.possession = svuPossession("Totals",self.year,self.seasonType,self.teamId)
    
    def getPullUpShootingStats(self):
        self.pullUp = svuPullUpShooting("Totals",self.year,self.seasonType,self.teamId)
        
    def getOffensiveReboundingStats(self):
        self.oreb = svuRebounding("Totals",self.year,self.seasonType,self.teamId,0)
    
    def getDefensiveReboundingStats(self):
        self.dreb = svuRebounding("Totals",self.year,self.seasonType,self.teamId,8)
        
    def getTotalReboundingStats(self):
        self.reb = svuRebounding("Totals",self.year,self.seasonType,self.teamId,16)
        
    def getAllReboundingStats(self):
        self.getOffensiveReboundingStats()
        self.getDefensiveReboundingStats()
        self.getTotalReboundingStats()
        
    def getMovementStats(self):
        self.movement = svuMovement("Totals",self.year,self.seasonType,self.teamId)
        
    def getElbowStats(self):
        self.elbow = svuTouchLocation("Totals",self.year,self.seasonType,self.teamId, "ElbowTouch")
    
    def getPostStats(self):
        self.post = svuTouchLocation("Totals",self.year,self.seasonType,self.teamId, "PostTouch")
        
    def getPaintStats(self):
        self.paint = svuTouchLocation("Totals",self.year,self.seasonType,self.teamId, "PaintTouch")
        
    def getAllSportsVUStats(self):
        self.getCatchAndShootStats()
        self.getDriveStats()
        self.getRimProtectionStats()
        self.getPassingStats()
        self.getPossessionStats()
        self.getPullUpShootingStats()
        self.getPullUpShootingStats()
        self.getAllReboundingStats()
        self.getMovementStats()
        self.getElbowStats()
        self.getPostStats()
        self.getPaintStats()
        
    #measureTypes = ["Base","Advanced","Misc","Four+Factors","Scoring","Opponent"]        
        
    def getTraditionalOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Base",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.traditionalOn = j2p(tUrl,1)
        self.traditionalOff = j2p(tUrl,2)
        
    def getAdvancedOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Advanced",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.advancedOn = j2p(tUrl,1)
        self.advancedOff = j2p(tUrl,2)
    
    def getMiscOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Misc",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.miscOn = j2p(tUrl,1)
        self.miscOff = j2p(tUrl,2)
        
    def getFourFactorsOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Four+Factors",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.fourFactorsOn = j2p(tUrl,1)
        self.fourFactorsOff = j2p(tUrl,2)
        
    def getScoringOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Scoring",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.scoringOn = j2p(tUrl,1)
        self.scoringOff = j2p(tUrl,2)
        
    def getOpponentOnOffStats(self):
        tUrl = url.teamOnOff.format(measureType="Opponent",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.opponentOn = j2p(tUrl,1)
        self.opponentOff = j2p(tUrl,2)
        
    def getAllOnOffStats(self):
        self.getTraditionalOnOffStats()
        self.getAdvancedOnOffStats()
        self.getMiscOnOffStats()
        self.getFourFactorsOnOffStats()
        self.getScoringOnOffStats()
        self.getOpponentOnOffStats()
        
    def getTraditionalLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Base",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.traditionalLienup = j2p(tUrl,1)
        
    def getAdvancedLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Advanced",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.advancedLineup = j2p(tUrl,1)
    
    def getMiscLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Misc",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.miscLineup = j2p(tUrl,1)
        
    def getFourFactorsLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Four+Factors",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.fourFactorsLineup = j2p(tUrl,1)
        
    def getScoringLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Scoring",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.scoringLineup = j2p(tUrl,1)
        
    def getOpponentLineupStats(self):
        tUrl = url.teamLineups.format(measureType="Opponent",perMode="Totals",year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.opponentLineup = j2p(tUrl,1)
        
    def getAllLineupStats(self):
        self.getTraditionalLineupStats()
        self.getAdvancedLineupStats()
        self.getMiscLineupStats()
        self.getFourFactorsLineupStats()
        self.getScoringLineupStats()
        self.getOpponentLineupStats()
        
    def getGameLogs(self):
        tUrl = url.gameLogs.format(year=self.year,seasonType=self.seasonType,teamId=self.teamId)
        self.gameLogs = j2p(tUrl,0)
        
    def getShotLogs(self):
        tUrl = url.shotLogs.format(year=self.year,seasonType=self.seasonType,teamId=self.teamId, playerId='0')
        self.shotLogs = j2p(tUrl,0)
            
hawks = team('1610612737','Regular+Season','2015-16')    