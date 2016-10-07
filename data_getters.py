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


def json_to_pandas_for_syngery(url):
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

# region General Stats

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
        general_url = "http://stats.nba.com/stats/leaguedash{teamOrPlayer}stats?" \
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

        return general_url.format(teamOrPlayer=self.playerOrTeam, college=self.college, conference=self.conference,
                                  country=self.country, dateFrom=self.dataFrom, dateTo=self.dateTo,
                                  division=self.division,
                                  draftPick=self.draftPick, draftYear=self.draftYear, gameScope=self.gameScope,
                                  gameSegment=self.gameSegment, height=self.height, lastNGames=self.lastNGames,
                                  leagueId=self.leagueId, location=self.location, measureType=self.measureType,
                                  month=self.month, opponentTeamId=self.opponentTeamId, outcome=self.outcome,
                                  poRound=self.poRound, paceAdjust=self.paceAdjust, perMode=self.perMode,
                                  period=self.period,
                                  playerExperience=self.playerExperience, playerPosition=self.playerPosition,
                                  plusMinus=self.plusMinus, rank=self.rank, seasonYear=self.season,
                                  seasonSegment=self.seasonSegment, seasonType=self.seasonType,
                                  shotClockRange=self.shotClockRange, starterBench=self.starterBench,
                                  teamId=self.teamId,
                                  vsConference=self.vsConference, vsDivision=self.vsDivision, weight=self.weight)


def get_general_stats(player_or_team, measure_type, per_mode, season_year, season_type):
    print(
        'Getting General ' + player_or_team + ' ' + measure_type + ' ' + per_mode + ' stats for the ' + get_year_string(
            season_year) + ' ' + season_type)

    file_path = '../data/' + player_or_team + '_data/' + get_year_string(
        season_year) + '_' + season_type + '_' + measure_type + '_' \
                + per_mode + '.csv'

    if not create_directories_and_check_for_file(file_path):
        print('GET DATA FROM WEB API')

        stats_url = GeneralStatsUrl(player_or_team=player_or_team, measure_type=measure_type, per_mode=per_mode,
                                    season=get_year_string(season_year), season_type=season_type)

        print(stats_url.build_url())
        df = json_to_pandas(stats_url.build_url(), 0)

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

# region Shot Data

class ShotDataUrl(object):
    def __init__(self, ahead_behind='', clutch_time='', context_filter='', context_measure='FGA', date_from='',
                 date_to='', end_period='', end_range='', game_id='', game_segment='', last_n_games='0',
                 league_id='00', location='', month='0', opponent_team_id='0', outcome='', period='0', player_id='0',
                 point_diff='', position='', range_type='', rookie_year='', season='2015-16',
                 season_type=SeasonTypes.REG, season_segment='', start_period='', start_range='', team_id='0',
                 vs_conference='', vs_division=''):
        self.aheadBehind = ahead_behind
        self.clutchTime = clutch_time
        self.contextFilter = context_filter
        self.contextMeasure = context_measure
        self.dateFrom = date_from
        self.dateTo = date_to
        self.endPeriod = end_period
        self.endRange = end_range
        self.gameId = game_id
        self.gameSegment = game_segment
        self.lastNGames = last_n_games
        self.leagueId = league_id
        self.location = location
        self.month = month
        self.opponentTeamId = opponent_team_id
        self.outcome = outcome
        self.period = period
        self.playerId = player_id
        self.pointDiff = point_diff
        self.position = position
        self.rangeType = range_type
        self.rookieYear = rookie_year
        self.season = season
        self.seasonType = season_type
        self.seasonSegment = season_segment
        self.startPeriod = start_period
        self.startRange = start_range
        self.teamId = team_id
        self.vsConference = vs_conference
        self.vsDivision = vs_division

    def build_url(self):
        shots_url = 'http://stats.nba.com/stats/shotchartdetail?' \
                    'AheadBehind={ahead_behind}&' \
                    'ClutchTime={clutch_time}&' \
                    'ContextFilter={context_filter}&' \
                    'ContextMeasure={context_measure}&' \
                    'DateFrom={date_from}&' \
                    'DateTo={date_to}&' \
                    'EndPeriod={end_period}&' \
                    'EndRange={end_range}&' \
                    'GameID={game_id}&' \
                    'GameSegment={game_segment}&' \
                    'LastNGames={last_n_games}&' \
                    'LeagueID={league_id}&' \
                    'Location={location}&' \
                    'Month={month}&' \
                    'OpponentTeamID={opponent_team_id}&' \
                    'Outcome={outcome}&' \
                    'Period={period}&' \
                    'PlayerID={player_id}&' \
                    'PointDiff={point_diff}&' \
                    'Position={position}&' \
                    'RangeType={range_type}&' \
                    'RookieYear={rookie_year}&' \
                    'Season={season}&' \
                    'SeasonType={season_type}&' \
                    'SeasonSegment={season_segment}&' \
                    'StartPeriodRange={start_period_range}&' \
                    'TeamID={team_id}&' \
                    'VsConference={vs_conference}&' \
                    'VsDivision={vs_division}'
        return shots_url.format(ahead_behind=self.aheadBehind, clutch_time=self.clutchTime,
                                context_filter=self.contextFilter, context_measure=self.contextMeasure,
                                date_from=self.dateFrom, date_to=self.dateTo, end_range=self.endRange,
                                end_period=self.endPeriod, season_segment=self.seasonSegment,
                                game_id=self.gameId, game_segment=self.gameSegment, last_n_games=self.lastNGames,
                                league_id=self.leagueId, location=self.location, month=self.month,
                                opponent_team_id=self.opponentTeamId, outcome=self.outcome, period=self.period,
                                player_id=self.playerId, point_diff=self.pointDiff, position=self.position,
                                range_type=self.rangeType, rookie_year=self.rookieYear, season=self.season,
                                season_type=self.seasonType, start_period_range=self.startPeriod, team_id=self.teamId,
                                vs_conference=self.vsConference, vs_division=self.vsDivision)


def get_shot_data(player_id='0', season_year=2015, season_type=SeasonTypes.REG, team_id='0', game_id='',
                  overwrite=False):
    print(player_id, season_year, season_type)
    print(
        'Getting Shot Data For ' + player_id + team_id + ' in the ' + get_year_string(season_year) + ' ' + season_type)
    fp_id = player_id + team_id + game_id

    file_path = '../data/shot_data/' + fp_id + '_' + get_year_string(season_year) + '_' + season_type + '.csv'
    print(file_path)

    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        print('GET DATA FROM WEB API')

        data_url = ShotDataUrl(player_id=player_id, season=get_year_string(season_year), season_type=season_type,
                               team_id=team_id, game_id=game_id)
        print (data_url.build_url())

        func_df = json_to_pandas(data_url.build_url(), 0)

        if func_df is not None:
            func_df.to_csv(file_path)
            print('GOT DATA FROM WEB API, WRITING TO FILE')
            return func_df

        else:
            print('COULD NOT GET DATA FROM WEB API')
            return None

    else:
        print('GETTING DATA FROM FILE')
        return pd.read_csv(file_path)


# endregion Shot Data


# region Play By Play

def get_pbp_data(game_id, season_year, season_type, overwrite=False):
    file_path = './data/play_by_play/' + game_id + '_' + season_year + '_' + season_type + '.csv'
    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        url = "http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&" \
              "EndRange=55800&" \
              "GameID={gameId}&" \
              "RangeType=2&" \
              "Season={seasonYear}&" \
              "SeasonType={seasonType}&" \
              "StartPeriod=1&S" \
              "tartRange=0"
        url = url.format(gameId=game_id, seasonYear=season_year, seasonType=season_type)
        func_df = json_to_pandas(url, 0)
        func_df.to_csv(file_path)
        return func_df
    else:
        return pd.read_csv(file_path)