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
    print(
        'Getting ' + player_or_team + ' synergy ' + offensive_or_defensive + ' ' + category + ' stats for ' + season_year)
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
    df = json_to_pandas_for_syngery(url)
    print(str(len(df)) + ' results')
    return df


synergy_play_types = ["Transition", "Isolation", "PRBallHandler", "PRRollman", "Postup", "Spotup", "Handoff", "Cut",
                      "OffScreen", "OffRebound", "Misc"]


def get_combined_synergy_stats_for_players(season_year='2016', offensive_or_defensive='offensive'):
    print('Getting all player synergy ' + offensive_or_defensive + ' stats for ' + season_year)
    df = pd.DataFrame(columns=['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB'])
    for play_type in synergy_play_types:
        play_type_df = get_synergy_stats(category=play_type, season_year=season_year,
                                         offensive_or_defensive=offensive_or_defensive)
        ppp_mean = float(play_type_df['Points'].sum()) / float(play_type_df['Poss'].sum())
        print(ppp_mean)
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
    print(str(len(df)) + ' total results')
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
    df = df.round(2)
    for ix, col in enumerate(columns):
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
