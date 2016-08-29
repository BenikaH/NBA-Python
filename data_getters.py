# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:48:48 2016

@author: pfenerty
"""

import pandas as pd
import json
import urllib2
import os.path


# region Utils


def json_to_pandas(url, index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        response = opener.open(url)
    except Exception:
        print('Could not get Stats')
        return None
    else:
        data = json.loads(response.read())
        headers = data['resultSets'][index]['headers']
        rows = data['resultSets'][index]['rowSet']
        data_dict = [dict(zip(headers, row)) for row in rows]
        return pd.DataFrame(data_dict)


def json_to_pandas_for_syngery(url, index):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        response = opener.open(url)
    except Exception:
        print('Could not get Stats')
        return None
    else:
        data = json.loads(response.read())
        data = data['results']
        if len(data) > 0:
            headers = data[0].keys()
            rows = [0] * len(data)
            for i in range(len(data)):
                rows[i] = data[i].values()
            data_dict = [dict(zip(headers, r)) for r in rows]
            return pd.DataFrame(data_dict)
        else:
            return pd.DataFrame()


def get_year_string(year):
    return str(year) + "-" + str(year + 1)[2:4]


def create_directories_and_check_for_file(filepath):
    split_path = filepath.split('/')
    current_path = ''
    for p in range(0, len(split_path) - 1):
        current_path += split_path[p] + '/'
        if not os.path.exists(current_path):
            os.makedirs(current_path)
    return os.path.isfile(filepath)


# endregion

# region Enums


class PlayerOrTeam(object):
    P = "player"
    T = "team"


class PerModes(object):
    TOTAL = "Totals"
    POSS = "PerPossession"
    PLAY = "PerPlay"
    MINUTE = "PerMinute"


class SeasonTypes(object):
    PRE = "Pre+Season"
    REG = "Regular+Season"
    PLAYOFF = "Playoffs"
    ALLSTAR = "All+Star"


class MeasureTypes(object):
    BASE = "Base"
    ADV = "Advanced"
    MISC = "Misc"
    SCORING = "Scoring"
    USAGE = "Usage"
    OPP = "Opponent"
    DEF = "Defense"


class SportsVUTypes(object):
    CATCH = "CatchShoot"
    DEF = "Defense"
    DRIVE = "Drives"
    PASS = "Passing"
    POSS = "Possessions"
    REB = "Rebounding"
    PULLUP = "PullUpShot"
    ELBOW = "ElbowTouch"
    POST = "PostTouch"
    PAINT = "PaintTouch"


class SynergyPlayTypes(object):
    TRANS = "Transition"
    ISO = "Isolation"
    PRB = "PRBallHandler"
    PRR = "PRRollman"
    POST = "Postup"
    SPOTUP = "Spotup"
    HANDOFF = "Handoff"
    CUT = "Cut"
    SCREEN = "OffScreen"
    REB = "OffRebound"
    MISC = "Misc"


class DistanceOrZone(object):
    D = "By+Zone"
    Z = "5ft+Range"


years = range(1996, 2016)
sports_vu_years = range(2013, 2016)


# endregion

class GeneralStatsUrl(object):
    def __init__(self, player_or_team='player', college='', conference='', country='', data_from='', date_to='',
                 division='', draft_pick='', draft_year='', game_scope='', game_segment='', height='', last_n_games='0',
                 league_id='00', location='', measure_type=MeasureTypes.BASE, month='0', opponenet_team_id='0',
                 outcome='', po_round='0', pace_adjust='N', per_mode=PerModes.TOTAL, period='0', player_experience='',
                 player_position='', plus_minus='N', rank='N', season='2015-16', season_segment='',
                 season_type=SeasonTypes.REG, shot_clock_range='', stater_bench='', team_id='0', vs_conference='',
                 vs_division='', weight=''):
        self.playerOrTeam = player_or_team
        self.college = college
        self.conference = conference
        self.country = country
        self.dataFrom = data_from
        self.dateTo = date_to
        self.division = division
        self.draftPick = draft_pick
        self.draftYear = draft_year
        self.gameScope = game_scope
        self.gameSegment = game_segment
        self.height = height
        self.lastNGames = last_n_games
        self.leagueId = league_id
        self.location = location
        self.measureType = measure_type
        self.month = month
        self.opponentTeamId = opponenet_team_id
        self.outcome = outcome
        self.poRound = po_round
        self.paceAdjust = pace_adjust
        self.perMode = per_mode
        self.period = period
        self.playerExperience = player_experience
        self.playerPosition = player_position
        self.plusMinus = plus_minus
        self.rank = rank
        self.season = season
        self.seasonSegment = season_segment
        self.seasonType = season_type
        self.shotClockRange = shot_clock_range
        self.starterBench = stater_bench
        self.teamId = team_id
        self.vsConference = vs_conference
        self.vsDivision = vs_division
        self.weight = weight

    def build_url(self):
        url = "http://stats.nba.com/stats/leaguedash{teamOrPlayer}stats?" \
              "College={college}&" \
              "Conference={conference}&" \
              "Country={country}&" \
              "DateFrom={dateFrom}&" \
              "DateTo={dateTo}&" \
              "Division={division}&" \
              "DraftPick={draftPick}&" \
              "DraftYear={draftYear}&" \
              "GameScope={gameScope}&" \
              "GameSegment={gameSegment}&" \
              "Height={height}&" \
              "LastNGames={lastNGames}&" \
              "LeagueID={leagueId}&" \
              "Location={location}&" \
              "MeasureType={measureType}&" \
              "Month={month}&" \
              "OpponentTeamID={opponentTeamId}&" \
              "Outcome={outcome}&" \
              "PORound={poRound}&" \
              "PaceAdjust={paceAdjust}&" \
              "PerMode={perMode}&" \
              "Period={period}&" \
              "PlayerExperience={playerExperience}&" \
              "PlayerPosition={playerPosition}&" \
              "PlusMinus={plusMinus}&" \
              "Rank={rank}&" \
              "Season={seasonYear}&" \
              "SeasonSegment={seasonSegment}&" \
              "SeasonType={seasonType}&" \
              "ShotClockRange={shotClockRange}&" \
              "StarterBench={starterBench}&" \
              "TeamID={teamId}&" \
              "VsConference={vsConference}&" \
              "VsDivision={vsDivision}&" \
              "Weight={weight}"

        return url.format(teamOrPlayer=self.playerOrTeam, college=self.college, conference=self.conference,
                          country=self.country, dateFrom=self.dataFrom, dateTo=self.dateTo, division=self.division,
                          draftPick=self.draftPick, draftYear=self.draftYear, gameScope=self.gameScope,
                          gameSegment=self.gameSegment, height=self.height, lastNGames=self.lastNGames,
                          leagueId=self.leagueId, location=self.location, measureType=self.measureType,
                          month=self.month, opponentTeamId=self.opponentTeamId, outcome=self.outcome,
                          poRound=self.poRound, paceAdjust=self.paceAdjust, perMode=self.perMode, period=self.period,
                          playerExperience=self.playerExperience, playerPosition=self.playerPosition,
                          plusMinus=self.plusMinus, rank=self.rank, seasonYear=self.season,
                          seasonSegment=self.seasonSegment, seasonType=self.seasonType,
                          shotClockRange=self.shotClockRange, starterBench=self.starterBench, teamId=self.teamId,
                          vsConference=self.vsConference, vsDivision=self.vsDivision, weight=self.weight)


# region General Stats


def get_general_stats(player_or_team, measure_type, per_mode, season_year, season_type):
    print(
        'Getting General ' + player_or_team + ' ' + measure_type + ' ' + per_mode + ' stats for the ' + get_year_string(
            season_year) + ' ' + season_type)

    file_path = '../data/' + player_or_team + '_data/' + season_year + '_' + season_type + '_' + measure_type + '_' \
                + per_mode + '.csv'

    if not create_directories_and_check_for_file(file_path):
        print('GET DATA FROM WEB API')

        url = "http://stats.nba.com/stats/leaguedash{teamOrPlayer}stats?" \
              "College=&" \
              "Conference=&" \
              "Country=&" \
              "DateFrom=&" \
              "DateTo=&" \
              "Division=&" \
              "DraftPick=&" \
              "DraftYear=&" \
              "GameScope=&" \
              "GameSegment=&" \
              "Height=&" \
              "LastNGames=0&" \
              "LeagueID=00&" \
              "Location=&" \
              "MeasureType={measureType}&" \
              "Month=0&" \
              "OpponentTeamID=0&" \
              "Outcome=&" \
              "PORound=0" \
              "&PaceAdjust=N&" \
              "PerMode={perMode}&" \
              "Period=0&" \
              "PlayerExperience=&" \
              "PlayerPosition=&" \
              "PlusMinus=N" \
              "&Rank=N&" \
              "Season={seasonYear}&" \
              "SeasonSegment=&" \
              "SeasonType={seasonType}&" \
              "ShotClockRange=&" \
              "StarterBench=" \
              "&TeamID=0&" \
              "VsConference=&" \
              "VsDivision=&" \
              "Weight="
        url = url.format(perMode=per_mode, seasonYear=season_year, seasonType=season_type, measureType=measure_type,
                         teamOrPlayer=player_or_team)

        df = json_to_pandas(url, 0)

        if df is not None:
            df.to_csv(file_path)
            print('GOT DATA FROM WEB API, WRITING TO FILE')
            return df

        else:
            print('COULD NOT GET DATA FROM WEB API')
            return None

    else:
        print('GETTING DATA FROM FILE')
        return pd.read_csv(file_path)


def get_all_general_stats():
    for year in years:
        year_string = get_year_string(year)
        for measure_type in MeasureTypes:
            for season_type in SeasonTypes:
                for per_mode in PerModes:
                    get_general_stats(PlayerOrTeam.P, measure_type, per_mode, year_string, season_type)
                    get_general_stats(PlayerOrTeam.T, measure_type, per_mode, year_string, season_type)


# endregion

# region Shot Location Stats


def get_shot_location_stats(player_or_team, per_mode, season_year, season_type):
    print(
        'Getting Shot Location ' + player_or_team + ' ' + per_mode + ' shot location stats for the '
        + get_year_string(season_year) + ' ' + season_type)

    if not os.path.exists('../data/' + player_or_team + '_data/'):
        os.makedirs('../data/' + player_or_team + '_data')
        print('MAKING DIRECTORY : ' + '../data/' + player_or_team + '_data')

    file_path = '../data/' + player_or_team + '_data/' + season_year + '_' + season_type + '_shot_location_' \
                + per_mode + '.csv'

    if not os.path.isfile(file_path):
        print('GETTING DATA FROM WEB API')
        url = "http://stats.nba.com/stats/leaguedash{playerOrTeam}shotlocations?" \
              "College=&" \
              "Conference=&" \
              "Country=&" \
              "DateFrom=&" \
              "DateTo=&" \
              "DistanceRange=5ft+Range&" \
              "Division=&" \
              "DraftPick=&" \
              "DraftYear=&" \
              "GameScope=&" \
              "GameSegment=&" \
              "Height=" \
              "&LastNGames=0&" \
              "LeagueID=00&" \
              "Location=&" \
              "MeasureType={measureType}&" \
              "Month=0&" \
              "OpponentTeamID=0&" \
              "Outcome=&" \
              "PORound=0&" \
              "PaceAdjust=N&" \
              "PerMode={perMode}&" \
              "Period=0&" \
              "PlayerExperience=&" \
              "PlayerPosition=&" \
              "PlusMinus=N&" \
              "Rank=N&" \
              "Season={seasonYear}&" \
              "SeasonSegment=&" \
              "SeasonType={seasonType}&" \
              "ShotClockRange=&" \
              "StarterBench=&" \
              "TeamID=0&" \
              "VsConference=&" \
              "VsDivision=&" \
              "Weight="
        url = url.format(playerOrTeam=player_or_team, measureType=MeasureTypes.BASE, perMode=per_mode,
                         seasonYear=season_year, seasonType=season_type)

        df = json_to_pandas(url, 0)

        if df is not None:
            print('GOT DATA FROM WEB API, WRITING TO FILE')
            df.to_csv("data\\" + player_or_team + "\\" + measure_type + "\\" + season_type + "\\" + per_mode + "\\" +
                      season_year + ".csv")
        else:
            print('COULD NOT GET DATA FROM WEB API')
            return None
    else:
        print('GETTING DATA FROM FILE')
        return pd.read_csv(file_path)


def get_all_player_shot_location_stats():
    for year in years:
        year_string = get_year_string(year)
        for measure_type in MeasureTypes:
            for season_type in SeasonTypes:
                for per_mode in PerModes:
                    print(year_string + ": " + measure_type + ", " + season_type + ", " + per_mode)
                    get_shot_location_stats(PlayerOrTeam.P, measure_type, per_mode, year_string, season_type)
                    get_shot_location_stats(PlayerOrTeam.T, measure_type, per_mode, year_string, season_type)


# endregion

# region SportsVU

def get_sports_vu_stats(team_or_player, vu_type, per_mode, season_year, season_type, opponent_id):
    if not os.path.exists('../data/' + team_or_player + '_data/'):
        os.makedirs('../data/' + team_or_player + '_data')
        print('MAKING DIRECTORY : ' + '../data/' + team_or_player + '_data')
    if not os.path.exists('../data/' + team_or_player + '_data/SportsVU'):
        os.makedirs('../data/' + team_or_player + '_data/SportsVU')
        print('MAKING DIRECTORY : ' + '../data/' + team_or_player + '_data/SPORTSVU')
    if opponent_id == '0':
        file_path = '../data/' + team_or_player + '_data/SportsVU/' + season_year + '_' + vu_type + '_' + \
                    season_type + '_' + per_mode
    else:
        file_path = '../data/' + team_or_player + '_data/SportsVU/' + season_year + '_' + vu_type + '_' + \
                    season_type + '_' + per_mode + '_Opp=' + str(opponent_id)
    if not os.path.isfile(file_path):
        print('FILE NOT FOUND, GETTING DATA FROM WEB API')
        url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
              "&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0" \
              "&OpponentTeamID={oppId}&Outcome=&PORound=0&PerMode={perMode}&PlayerExperience=&PlayerOrTeam={playerOrTeam}" \
              "&PlayerPosition=&PtMeasureType={vuType}&Season={seasonYear}&SeasonSegment=&SeasonType={seasonType}" \
              "&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
        url = url.format(playerOrTeam=team_or_player, vuType=vu_type, seasonYear=season_year, seasonType=season_type,
                         perMode=per_mode, oppId=opponent_id)
        df = json_to_pandas(url, 0)
        if df is not None:
            df.to_csv(file_path)
            return df
    else:
        print('FILE FOUND, READING DATA FROM FILE')
        return pd.read_csv(file_path)


def get_all_sports_vu_stats():
    for year in range(2013, 2015):
        year_string = get_year_string(year)
        for vu_type in SportsVUTypes:
            for season_type in SeasonTypes:
                for per_mode in PerModes:
                    print(year_string + ": " + vu_type + ", " + season_type + ", " + per_mode)
                    get_sports_vu_stats("player", vu_type, per_mode, year_string, season_type)


# endregion

# region Synergy

def get_synergy_stats(team_or_player, synergy_play_type, offense_or_defense):
    if not os.path.exists('../data/' + team_or_player.title() + '_data/'):
        os.makedirs('../data/' + team_or_player.title() + '_data')
        print('MAKING DIRECTORY : ' + './data/' + team_or_player.title() + '_data')
    if not os.path.exists('../data/' + team_or_player.title() + '_data/Synergy'):
        os.makedirs('../data/' + team_or_player.title() + '_data/Synergy')
        print('MAKING DIRECTORY : ' + './data/' + team_or_player.title() + '_data/Synergy')
    file_path = '../data/' + team_or_player.title() + '_data/Synergy/' + synergy_play_type + "_" + offense_or_defense + \
                '_2015-16.csv'
    if not os.path.isfile(file_path):
        print('FILE NOT FOUND, GETTING DATA FROM WEB API')
        url = "http://stats-prod.nba.com/wp-json/statscms/v1/synergy/{teamOrPlayer}/?category={playType}&limit=500" \
              "&name={offenseOrDefense}&q=2449554&season=2015&seasonType=Reg"
        url = url.format(teamOrPlayer=team_or_player, playType=synergy_play_type, offenseOrDefense=offense_or_defense)
        data_df = json_to_pandas_for_syngery(url, 0)
        data_df.to_csv(file_path)
        return data_df
    else:
        return pd.read_csv(file_path)


# endregion

# region Game Logs

def get_player_game_logs(season_year, season_type, player_name, player_id):
    if not os.path.exists('../data/player_data/'):
        os.makedirs('../data/player_data')
        print('MAKING DIRECTORY : ' + '../data/player_data')
    if not os.path.exists('../data/player_data/game_logs'):
        os.makedirs('../data/player_data/game_logs')
        print('MAKING DIRECTORY : ' + '../data/player_data/game_logs')
    file_path = '../data/player_data/game_logs/' + season_year + '_' + season_type + '_' + player_name + '.csv'
    if not os.path.isfile(file_path):
        print("GETTING " + player_name + "'s Game Logs for the " + season_year + " " + season_type + " FROM WEB API!")
        url = "http://stats.nba.com/stats/playergamelog?" \
              "LeagueID=00&" \
              "PlayerID={pid}&" \
              "Season={seasonYear}&" \
              "SeasonType={seasonType}"
        url = url.format(pid=player_id, seasonYear=season_year, seasonType=season_type)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        print("ALREADY HAVE " + player_name + "'s Game Logs for the " + season_year + " " + season_type + " ON FILE!")
        return pd.read_csv(file_path)


# endregion

# region Passing

def get_player_passing_dashboard(player_id, season_year):
    if not os.path.exists('../data/player_data/'):
        os.makedirs('../data/player_data')
        print('MAKING DIRECTORY : ' + './data/player_data')
    if not os.path.exists('../data/player_data/passing'):
        os.makedirs('../data/player_data/passing')
        print('MAKING DIRECTORY : ' + './data/player_data/passing')
    file_path = '../data/player_data/passing/' + str(player_id) + '_' + season_year + '.csv'
    if not os.path.isfile(file_path):
        print('FILE NOT FOUND, GETTING DATA FROM WEB API')
        url = 'http://stats.nba.com/stats/playerdashptpass?' \
              'DateFrom=&' \
              'DateTo=&' \
              'GameSegment=&' \
              'LastNGames=0&' \
              'LeagueID=00&' \
              'Location=&' \
              'Month=0&' \
              'OpponentTeamID=0&' \
              'Outcome=&' \
              'PerMode=Totals&' \
              'Period=0&' \
              'PlayerID={playerId}&' \
              'Season={seasonYear}&' \
              'SeasonSegment=&' \
              'SeasonType=Regular+Season&' \
              'TeamID=0&' \
              'VsConference=&' \
              'VsDivision='
        url = url.format(playerId=player_id, seasonYear=season_year)
        data_df = json_to_pandas(url, 1)
        if data_df is not None:
            data_df.to_csv(file_path)
            return data_df
        else:
            print('FILE IS NONE')
            return None
    else:
        print('FILE FOUND, READING FROM FILE')
        return pd.read_csv(file_path)


# endregion


url = GeneralStatsUrl()
print(url.build_url())
