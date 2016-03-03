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
    teamInfo = "http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType={seasonType}&TeamID={teamId}"\
               "&season={year}"
    teamRoster = "http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season={year}&TeamID={teamId}"
    teamStats = "http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=" \
                "&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType={measureType}&Month=0&OpponentTeamID=" \
                "0&Outcome=&PORound=0&PaceAdjust=N&PerMode={perMode}&Period=0&PlayerExperience=&PlayerPosition=&Plu" \
                "sMinus=N&Rank=N&Season={year}&SeasonSegment=&SeasonType={seasonType}&ShotClockRange=&StarterBench=" \
                "&TeamID={teamId}&VsConference=&VsDivision="
    #teamId is a 10 digit unique identifier
    #measureType comes from the measureTypes paramEnum
    #year is in the format 2015-16
    #seasonType => [Regular+Season,Pre+Season,Playoffs,All-Star]
    #perMode => [PerGame,Per100Possessions,Totals,Per100Plays,Per48,Per36,Per30,PerMinute,PerPossession,PerPlay,MinutesPer]
    synergy = "http://stats.nba.com/js/data/playtype/{playerOrTeam}_{playType}.js"
    sportsVU = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=" \
               "&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0" \
               "&Outcome=&PORound=0&PerMode={perMode}&PlayerExperience=&PlayerOrTeam=Team&PlayerPosition=&PtMeasureType=" \
               "{playType}&Season={year}&SeasonSegment=&SeasonType={seasonType}&StarterBench=&TeamID={teamId}&VsConference=" \
               "&VsDivision=&Weight="

class paramEnums:
    seasonTypes = ["Regular+Season","Pre+Season","Playoffs","All-Star"]
    perModes = ["PerGame","Per100Possessions","Totals","Per100Plays","Per48","Per36","Per30","PerMinute","PerPossession","PerPlay,MinutesPer"]     
    measureTypes = ["Base","Advanced","Misc","Four+Factors","Scoring","Opponenet"]
    play_types=["PRBallHandler","Cut","Handoff","Isolation","Misc","OffScreen","Postup","OffRebound","PRRollMan","Spotup","Transition"]
    
class traditionalStats:
    def __init__(self,teamId,year,seasonType, measureType):
        tradURL = url.teamStats.format(teamId=teamId, perMode="Totals", measureType=measureType, year=year, seasonType=seasonType)
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

class svuCatchAndShoot:
    def __init__(self,perMode,year,seasonType,teamId):
            casUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="CatchShoot")
            data = getJson(casUrl,0)
            data = data[0]
            self.fgm = data[7]
            self.fga = data[8]
            self.pts = data[10]
            self.fg3m = data[11]
            self.fg3a = data[12]
            
class svuDefense:
    def __init__(self,perMode,year,seasonType,teamId):
            dUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="Defense")
            data = getJson(dUrl,0)
            data = data[0]
            self.rimFga = data[10]
            self.rimFgm = data[11]
            
class svuDrives:
    def __init__(self,perMode,year,seasonType,teamId):
            drivesUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="Drives")
            data = getJson(drivesUrl,0)
            data = data[0]
            self.drives = data[7]
            self.fgm = data[8]
            self.fga = data[9]
            self.ftm = data[11]
            self.fta = data[12]
            self.points = data[14]
            self.pointsPct = data[15]
            self.passes = data[16]
            self.passPct = data[17]
            self.ast = data[18]
            self.astPct = data[19]
            self.tov = data[20]
            self.tovPct = data[21]
            self.pf = data[22]
            self.pfPct = data[23]
            
class svuPassing:
    def __init__(self,perMode,year,seasonType,teamId):
            passUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="Passing")
            data = getJson(passUrl,0)
            data = data[0]
            self.made = data[7]
            self.recieved = data[8]
            self.ftAst = data[10]
            self.secAst = data[11]
            self.potAst = data[12]
            self.astPointsCreated = data[13]
            self.adjAst = data[14]
            self.astToPass = data[15]
            self.astToPassAdj = data[16]
            
class svuPossession:
    def __init__(self,perMode,year,seasonType,teamId):
            possUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="Possessions")
            data = getJson(possUrl,0)
            data = data[0]
            self.touches = data[8]
            self.frontCtTouches = data[9]
            self.timeOfPoss = data[10]
            self.secPerTouch = data[11]
            self.dribblePerTouch = data[12]
            self.ptsPerTouch = data[13]
            self.elbowTouches = data[14]
            self.postTouches = data[15]
            self.paintTouches = data[16]
            self.pointsPerElbowTouch = data[17]
            self.pointsPerPostTouch = data[18]
            self.pointsPerPaintTouch = data[19]
            
class svuPullUpShooting:
    def __init__(self,perMode,year,seasonType,teamId):
            pullUpUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="PullUpShot")
            data = getJson(pullUpUrl,0)
            data = data[0]
            self.fgm = data[7]
            self.fga = data[8]
            self.pts = data[10]
            self.fg3m = data[11]
            self.fg3a = data[12]
            
class svuRebounding:
    def __init__(self,perMode,year,seasonType,teamId,index):
            rebUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="Rebounding")
            data = getJson(rebUrl,0)
            data = data[0]
            self.Contest = data[8+index]
            self.Uncontest = data[9+index]
            self.Chances = data[11+index]
            self.Deferred = data[13+index]
            self.avDist = data[15+index]
            
class svuMovement:
    def __init__(self,perMode,year,seasonType,teamId):
            movUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType="SpeedDistance")
            data = getJson(movUrl,0)
            data = data[0]
            self.distFeet = data[8]
            self.distOMiles = data[10]
            self.distDMiles = data[11]
            self.avSpeed = data[12]
            self.avSpeedO = data[13]
            self.avSpeedD = data[14]
            
class svuTouchLocation:
    def __init__(self,perMode,year,seasonType,teamId,location):
            locUrl = url.sportsVU.format(perMode=perMode,year=year,seasonType=seasonType,teamId=teamId,playType=location)
            data = getJson(locUrl,0)
            data = data[0]
            self.touches = data[9]
            self.fgm = data[10]
            self.fga = data[11]
            self.ftm = data[13]
            self.fta = data[14]
            self.pts = data[16]
            self.passes = data[18]
            self.ast = data[20]
            self.tov = data[22]
            self.pf = data[24]            

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
        self.traditional = traditionalStats(self.teamId, self.year, self.seasonType, "Base")
        
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
    
hawks = team('1610612737','Regular+Season','2015-16')    