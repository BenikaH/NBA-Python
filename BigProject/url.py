# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:41:37 2016

@author: pfenerty
"""

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
               
    teamOnOff = "http://stats.nba.com/stats/teamplayeronoffdetails?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00"\
                "&Location=&MeasureType={measureType}&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode={perMode}&Period=0&PlusMinus=N"\
                "&Rank=N&Season={year}&SeasonSegment=&SeasonType={seasonType}&TeamID={teamId}&VsConference=&VsDivision="
                
    teamLineups = "http://stats.nba.com/stats/teamdashlineups?DateFrom=&DateTo=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00"\
                  "&Location=&MeasureType={measureType}&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode={perMode}&Period=0&PlusMinus=N&Rank=N&"\
                  "Season={year}&SeasonSegment=&SeasonType={seasonType}&TeamID={teamId}&VsConference=&VsDivision="
                  
    gameLogs = "http://stats.nba.com/stats/teamgamelog?LeagueID=00&Season={year}&SeasonType={seasonType}&TeamID={teamId}"
    shotLogs = "http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS={year}&ContextFilter=&ContextMeasure=FGA&DateFrom="\
               "&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome="\
               "&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID={playerId}&PlusMinus=N&Position=&Rank=N&RookieYear=&Season={year}&SeasonSegment="\
               "&SeasonType={seasonType}&TeamID={teamId}&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0"
               