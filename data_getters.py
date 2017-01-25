import pandas as pd
import json
import urllib2
import os.path
import sys


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

def get_general_stats(player_or_team='player', measure_type='Base', per_mode='Totals', season_year='2016-17'):
    url = 'http://stats.nba.com/stats/leaguedash{player_or_team}stats?' \
          'Conference=&' \
          'DateFrom=&' \
          'DateTo=&' \
          'Division=&' \
          'GameScope=&' \
          'GameSegment=&' \
          'LastNGames=0&' \
          'LeagueID=00&' \
          'Location=&' \
          'MeasureType={measure_type}&' \
          'Month=0' \
          '&OpponentTeamID=0' \
          '&Outcome=&' \
          'PORound=0&' \
          'PaceAdjust=N&' \
          'PerMode={per_mode}&' \
          'Period=0&' \
          'PlayerExperience=&' \
          'PlayerPosition=&' \
          'PlusMinus=N&' \
          'Rank=N&' \
          'Season={season_year}&' \
          'SeasonSegment=&' \
          'SeasonType=Regular+Season&' \
          'ShotClockRange=&' \
          'StarterBench=&' \
          'TeamID=0&' \
          'VsConference=&' \
          'VsDivision='
    url = url.format(player_or_team=player_or_team, measure_type=measure_type, per_mode=per_mode,
                     season_year=season_year)
    return json_to_pandas(url, 0)


def get_synergy_stats(player_or_team='player', category='Transition', offensive_or_defensive='offensive',
                      season_year='2016'):
    url = 'http://stats-prod.nba.com/wp-json/statscms/v1/synergy/' \
          '{player_or_team}/?' \
          'category={category}&' \
          'limit=500&' \
          'name={offensive_or_defensive}&' \
          'q=2471454&' \
          'season={season_year}&' \
          'seasonType=Reg'
    url = url.format(player_or_team=player_or_team, category=category, offensive_or_defensive=offensive_or_defensive,
                     season_year=season_year)
    return json_to_pandas_for_syngery(url)


synergy_play_types = ["Transition", "Isolation", "PRBallHandler", "PRRollman", "Postup", "Spotup", "Handoff", "Cut",
                      "OffScreen", "OffRebound", "Misc"]


def get_combined_synergy_stats_for_players(season_year='2016', offensive_or_defensive='offensive'):
    df = pd.DataFrame(columns=['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB'])
    for play_type in synergy_play_types:
        play_type_df = get_synergy_stats(category=play_type, season_year=season_year,
                                         offensive_or_defensive=offensive_or_defensive)
        ppp_mean = float(play_type_df['Points'].sum()) / float(play_type_df['Poss'].sum())
        play_type_df['PPP_ABOVE_MEAN'] = play_type_df['PPP'] - ppp_mean
        play_type_df['EXP_PTS'] = ppp_mean * play_type_df['Poss']
        play_type_df = play_type_df[
            ['PlayerIDSID', 'TeamIDSID', 'PlayerFirstName', 'PlayerLastName', 'TeamNameAbbreviation', 'Poss', 'Points',
             'Time', 'TO', 'PlusOne', 'PPP', 'PPP_ABOVE_MEAN', 'EXP_PTS']]
        play_type_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB',
                                play_type + '_POSS', play_type + '_PTS', play_type + '_FREQ', play_type + '_TOV',
                                play_type + '_AND_ONE', play_type + '_PPP', play_type + '_PPP_ABOVE_MEAN',
                                play_type + '_EXP_PTS']
        df = df.merge(play_type_df, on=['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB'],
                      how='outer')
    df = df.fillna(0)
    df['Total_POSS'] = 0
    df['Total_PTS'] = 0
    df['Total_FREQ'] = 0
    df['Total_TOV'] = 0
    df['Total_AND_ONE'] = 0
    for play_type in synergy_play_types:
        df['Total_POSS'] += df[play_type + '_POSS']
        df['Total_PTS'] += df[play_type + '_PTS']
        df['Total_FREQ'] += df[play_type + '_FREQ']
        df['Total_TOV'] += df[play_type + '_TOV']
        df['Total_AND_ONE'] = df[play_type + '_AND_ONE']
    df['Total_PPP'] = df['Total_PTS'] / df['Total_POSS']
    return df


def get_game_logs_for_player(player_id, season_year='2016-17'):
    url = 'http://stats.nba.com/stats/playergamelog?' \
          'DateFrom=&' \
          'DateTo=&' \
          'LeagueID=00&' \
          'PlayerID={player_id}&' \
          'Season={season_year}&' \
          'SeasonType=Regular+Season'
    url = url.format(player_id=player_id, season_year=season_year)
    return json_to_pandas(url, 0)


def print_reddit_table(df, columns):
    for ix, col in enumerate(columns):
        try:
            df[col] = df[col].round(2)
        except TypeError:
            2 + 2
        sys.stdout.write(col + (' | ' if ix is not len(columns) - 1 else ''))
    print('')
    for ix, col in enumerate(columns):
        sys.stdout.write(':--' + (' | ' if ix is not len(columns) - 1 else ''))
    print('')
    for ix, row in df.iterrows():
        for jx, col in enumerate(columns):
            try:
                sys.stdout.write(str(row[col]) + (' | ' if jx is not len(columns) - 1 else ''))
            except UnicodeEncodeError:
                sys.stdout.write(' ' + (' | ' if jx is not len(columns) - 1 else ''))
        print('')


def get_player_passes(player_id, season_year='2016-17'):
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
          'PORound=0&' \
          'PerMode=Totals&' \
          'Period=0&' \
          'PlayerID={player_id}' \
          '&Season={season_year}&' \
          'SeasonSegment=&' \
          'SeasonType=Regular+Season&' \
          'TeamID=0&' \
          'VsConference=&' \
          'VsDivision='
    url = url.format(player_id=player_id, season_year=season_year)
    return json_to_pandas(url, 0)


defender_distance_ranges = ['0-2+Feet+-+Very+Tight', '2-4+Feet+-+Tight', '4-6+Feet+-+Open', '6%2B+Feet+-+Wide+Open']
dribble_ranges = ['0+Dribbles', '1+Dribble', '2+Dribbles', '3-6+Dribbles', '7%2B+Dribbles']


def get_shooting_breakdown_stats(defender_distance='', season_year='2016-17', dribble_range=''):
    url = 'http://stats.nba.com/stats/leaguedashplayerptshot?' \
          'CloseDefDistRange={defender_distance}&' \
          'College=&' \
          'Conference=&' \
          'Country=&' \
          'DateFrom=&' \
          'DateTo=&' \
          'Division=&' \
          'DraftPick=&' \
          'DraftYear=&' \
          'DribbleRange={dribble_range}&' \
          'GameScope=&' \
          'GameSegment=&' \
          'GeneralRange=&' \
          'Height=&' \
          'LastNGames=0&' \
          'LeagueID=00&' \
          'Location=&' \
          'Month=0&' \
          'OpponentTeamID=0&' \
          'Outcome=&' \
          'PORound=0&' \
          'PaceAdjust=N&' \
          'PerMode=Totals&' \
          'Period=0&' \
          'PlayerExperience=&' \
          'PlayerPosition=&' \
          'PlusMinus=N&' \
          'Rank=N&Season={season_year}&' \
          'SeasonSegment=&' \
          'SeasonType=Regular+Season&' \
          'ShotClockRange=&' \
          'ShotDistRange=&' \
          'StarterBench=&' \
          'TeamID=0&' \
          'TouchTimeRange=&' \
          'VsConference=&' \
          'VsDivision=&' \
          'Weight='
    url = url.format(defender_distance=defender_distance, season_year=season_year, dribble_range=dribble_range)
    return json_to_pandas(url, 0)


def shotchartdetail(year='2016-17', player_id='0', team_id='0', overwrite=False):
    file_path = './data/shotchartdetail/' + str(player_id) + '-' + str(team_id) + '.csv'
    if (not create_directories_and_check_for_file(filepath=file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/shotchartdetail?' \
              'AheadBehind=&' \
              'CFID=33&' \
              'CFPARAMS={year}&' \
              'ClutchTime=&' \
              'Conference=&' \
              'ContextFilter=&' \
              'ContextMeasure=FGA&' \
              'DateFrom=&DateTo=&' \
              'Division=&' \
              'EndPeriod=10&' \
              'EndRange=28800&' \
              'GameEventID=&' \
              'GameID=&' \
              'GameSegment=&' \
              'GroupID=&' \
              'GroupQuantity=5&' \
              'LastNGames=0&' \
              'LeagueID=00&' \
              'Location=&' \
              'Month=0&' \
              'OpponentTeamID=0&' \
              'Outcome=&' \
              'PORound=0&' \
              'Period=0&' \
              'PlayerID={player_id}&' \
              'PlayerPosition=&' \
              'PointDiff=&' \
              'Position=&' \
              'RangeType=0&' \
              'RookieYear=&' \
              'Season=2016-17&' \
              'SeasonSegment=&' \
              'SeasonType=Regular+Season&' \
              'ShotClockRange=&' \
              'StartPeriod=1&' \
              'StartRange=0&' \
              'StarterBench=&' \
              'TeamID={team_id}&' \
              'VsConference=&' \
              'VsDivision='
        url = url.format(year=year, player_id=player_id, team_id=team_id)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


def leaguegamelog(year='2016-17', overwrite=False):
    file_path = './data/leaguegamelog/' + str(year) + '.csv'
    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/leaguegamelog?' \
              'Counter=1000&' \
              'DateFrom=&' \
              'DateTo=&' \
              'Direction=DESC&' \
              'LeagueID=00&' \
              'PlayerOrTeam=T&' \
              'Season={year}&' \
              'SeasonType=Regular+Season&' \
              'Sorter=DATE'
        url = url.format(year=year)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


def playbyplayv2(game_id, year='2016-17', overwrite=False):
    file_path = './data/playbyplayv2/' + str(year) + '/' + str(game_id) + '.csv'
    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/playbyplayv2?' \
              'EndPeriod=10&' \
              'EndRange=55800&' \
              'GameID={game_id}&' \
              'RangeType=2&' \
              'Season={year}&' \
              'SeasonType=Regular+Season&' \
              'StartPeriod=1&' \
              'StartRange=0'
        url = url.format(game_id=game_id, year=year)
        print(url)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Sports VU
def leaguedashpstats(pt_measure_type, season_year='2016-17', overwrite=False):
    file_path = './data/leaguedashpstats/' + str(pt_measure_type) + '/' + str(season_year) + '.csv'
    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/leaguedashptstats?' \
              'College=&' \
              'Conference=&' \
              'Country=&' \
              'DateFrom=&' \
              'DateTo=&' \
              'Division=&' \
              'DraftPick=&' \
              'DraftYear=&' \
              'GameScope=&' \
              'Height=&' \
              'LastNGames=0&' \
              'LeagueID=00&' \
              'Location=&Month=0&' \
              'OpponentTeamID=0&' \
              'Outcome=&' \
              'PORound=0&' \
              'PerMode=Totals&' \
              'PlayerExperience=&' \
              'PlayerOrTeam=Player&' \
              'PlayerPosition=&' \
              'PtMeasureType={pt_measure_type}&' \
              'Season={season_year}&' \
              'SeasonSegment=&' \
              'SeasonType=Regular+Season&' \
              'StarterBench=&' \
              'TeamID=0&' \
              'VsConference=&' \
              'VsDivision=&' \
              'Weight='
        url = url.format(pt_measure_type=pt_measure_type, season_year=season_year)
        print(url)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


def teamplayeronoffdetails(team_id, measure_type='Base', season_year='2016-17'):
    url = 'http://stats.nba.com/stats/teamplayeronoffdetails?DateFrom=&' \
          'DateTo=&' \
          'GameSegment=&' \
          'LastNGames=0&' \
          'LeagueID=00&' \
          'Location=&' \
          'MeasureType={measure_type}&' \
          'Month=0&' \
          'OpponentTeamID=0&' \
          'Outcome=&' \
          'PaceAdjust=N&' \
          'PerMode=Totals&' \
          'Period=0&' \
          'PlusMinus=N&' \
          'Rank=N&' \
          'Season={season_year}&' \
          'SeasonSegment=&' \
          'SeasonType=Regular+Season&' \
          'TeamID={team_id}&' \
          'VsConference=&' \
          'VsDivision='
    url = url.format(season_year=season_year, team_id=team_id, measure_type=measure_type)
    return json_to_pandas(url, 1)


def get_all_player_on_data(season_year='2016-17', measure_type='Base', overwrite=False):
    file_path = './data/teamplayeronoffdetails/' + '/' + str(measure_type) + '_' + str(season_year) + '.csv'
    if (not create_directories_and_check_for_file(file_path)) or overwrite:
        team_ids = get_general_stats(season_year=season_year)['TEAM_ID'].unique()
        df = pd.DataFrame()
        for team_id in team_ids:
            print(team_id)
            df = df.append(teamplayeronoffdetails(team_id, season_year=season_year, measure_type=measure_type))
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


