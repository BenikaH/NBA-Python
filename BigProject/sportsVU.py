# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:55:21 2016

@author: pfenerty
"""
from dataGetters import getJson
from url import url

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
