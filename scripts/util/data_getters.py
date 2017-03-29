import json
import os.path
import sys
import urllib.request

import pandas as pd


# region Utils


def json_to_pandas(url, index=0):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Referer', 'http://stats.nba.com/leaders/')]
    try:
        response = opener.open(url)
    except Exception:
        print(Exception)
        return Exception
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
        print(Exception)
        return Exception
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


def file_exists(filepath):
    split_path = filepath.split('/')
    current_path = ''
    for p in range(0, len(split_path) - 1):
        current_path += split_path[p] + '/'
        if not os.path.exists(current_path):
            os.makedirs(current_path)
    return os.path.isfile(filepath)


def print_reddit_table(df, columns):
    for ix, col in enumerate(columns):
        try:
            df[col] = df[col].round(2)
        except TypeError:
            print(TypeError)
        sys.stdout.write(str(col) + (' | ' if ix is not len(columns) - 1 else ''))
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


# endregion

# Gets traditional stats for players
def leaguedashplayerstats(measure_type='Base', per_mode='Totals', season_year='2016-17', date_from='', date_to='',
                          overwrite=True):
    file_path = '../../data/leaguedashplayerstats/' + season_year + '/' + measure_type + '/' + per_mode + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/leaguedashplayerstats?' \
              'Conference=&' \
              'DateFrom={date_from}&' \
              'DateTo={date_to}&' \
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
        url = url.format(measure_type=measure_type, per_mode=per_mode, season_year=season_year, date_from=date_from,
                         date_to=date_to)
        print(url)
        df = json_to_pandas(url, 0)
        if date_from == '' and date_to == '':
            df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Gets synergy stats for players or teams for a year and specific play type
def synergyapi(category, player_or_team='player', offensive_or_defensive='offensive', season_year='2016',
               overwrite=True):
    file_path = '../../data/synergy/' + player_or_team + '/' + offensive_or_defensive + '/' + get_year_string(
        season_year) + '/' + category + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats-prod.nba.com/wp-json/statscms/v1/synergy/' \
              '{player_or_team}/?' \
              'category={category}&' \
              'limit=500&' \
              'name={offensive_or_defensive}&' \
              'q=2471454&' \
              'season={season_year}&' \
              'seasonType=Reg'
        url = url.format(player_or_team=player_or_team, category=category,
                         offensive_or_defensive=offensive_or_defensive, season_year=season_year)
        df = json_to_pandas_for_syngery(url)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


synergy_play_types = ["Transition", "Isolation", "PRBallHandler", "PRRollman", "Postup", "Spotup", "Handoff", "Cut",
                      "OffScreen", "OffRebound", "Misc"]


# Gets synergy stats for players for all play types aggregated
def allsynergy(offensive_or_defensive='offensive', season_year='2016', overwrite=True):
    file_path = '../../data/synergy/player/' + offensive_or_defensive + '/' + get_year_string(season_year) + '/All.csv'
    if (not file_exists(file_path)) or overwrite:
        df = pd.DataFrame(columns=['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB'])
        for play_type in synergy_play_types:
            play_type_df = synergyapi(category=play_type, season_year=season_year,
                                      offensive_or_defensive=offensive_or_defensive)
            ppp_mean = float(play_type_df['Points'].sum()) / float(play_type_df['Poss'].sum())
            play_type_df['PPP_ABOVE_MEAN'] = play_type_df['PPP'] - ppp_mean
            play_type_df['EXP_PTS'] = ppp_mean * play_type_df['Poss']
            play_type_df = play_type_df[
                ['PlayerIDSID', 'TeamIDSID', 'PlayerFirstName', 'PlayerLastName', 'TeamNameAbbreviation', 'Poss',
                 'Points',
                 'Time', 'TO', 'PlusOne', 'PPP', 'PPP_ABOVE_MEAN', 'EXP_PTS']]
            play_type_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB',
                                    play_type + '_POSS', play_type + '_PTS', play_type + '_FREQ', play_type + '_TOV',
                                    play_type + '_AND_ONE', play_type + '_PPP', play_type + '_PPP_ABOVE_MEAN',
                                    play_type + '_EXP_PTS']
            df = df.merge(play_type_df,
                          on=['PLAYER_ID', 'TEAM_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ABB'],
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
    else:
        return pd.read_csv(file_path)


# Gets a players game logs
def playergamelog(player_id, season_year='2016-17', overwrite=True):
    file_path = '../../data/playergamelog/' + season_year + '/' + player_id + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/playergamelog?' \
              'DateFrom=&' \
              'DateTo=&' \
              'LeagueID=00&' \
              'PlayerID={player_id}&' \
              'Season={season_year}&' \
              'SeasonType=Regular+Season'
        url = url.format(player_id=player_id, season_year=season_year)
        print(url)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Gets a players passing dashboard (Details passes to other players)
def playerdashptpass(player_id, season_year='2016-17', overwrite=True):
    file_path = '../../data/playerdashptpass/' + season_year + '/' + player_id + '.csv'
    if (not file_exists(file_path)) or overwrite:
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
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


defender_distance_ranges = ['0-2+Feet+-+Very+Tight', '2-4+Feet+-+Tight', '4-6+Feet+-+Open', '6%2B+Feet+-+Wide+Open']
dribble_ranges = ['0+Dribbles', '1+Dribble', '2+Dribbles', '3-6+Dribbles', '7%2B+Dribbles']


# Gets a players shot details by defender distance or number of dribbles
def leaguedashplayerptshot(season_year='2016-17', defender_distance='', dribble_range='', overwrite=True):
    file_path = '../../data/leaguedashplayerptshot/' + season_year + '/' + defender_distance + '_' + dribble_range + '.csv'
    if (not file_exists(file_path)) or overwrite:
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
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Gets a players shot details (player_id / team_id = 0 returns all players)
def shotchartdetail(year='2016-17', player_id='0', team_id='0', overwrite=True):
    file_path = '../../data/shotchartdetail/' + year + '/' + str(player_id) + '-' + str(team_id) + '.csv'
    if (not file_exists(filepath=file_path)) or overwrite:
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
              'Season={season}&' \
              'SeasonSegment=&' \
              'SeasonType=Regular+Season&' \
              'ShotClockRange=&' \
              'StartPeriod=1&' \
              'StartRange=0&' \
              'StarterBench=&' \
              'TeamID={team_id}&' \
              'VsConference=&' \
              'VsDivision='
        url = url.format(year=year, player_id=player_id, team_id=team_id, season=year)
        print(url)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Gets game log for entire league for a season
def leaguegamelog(year='2016-17', overwrite=True):
    file_path = '../../data/leaguegamelog/' + str(year) + '.csv'
    if (not file_exists(file_path)) or overwrite:
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


# Gets play by play for a game
def playbyplayv2(game_id, year='2016-17', overwrite=True):
    if len(str(game_id)) < 10:
        game_id = '00' + str(game_id)
    file_path = '../../data/playbyplayv2/' + str(year) + '/' + str(game_id) + '.csv'
    if (not file_exists(file_path)) or overwrite:
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
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        df = pd.read_csv(file_path)
        if len(df) < 200:
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
            df = json_to_pandas(url, 0)
            df.to_csv(file_path)
        return df


# Gets SportsVU stats for a play type and season
def leaguedashpstats(pt_measure_type, season_year='2016-17', date_from='', date_to='', overwrite=False):
    file_path = '../../data/leaguedashpstats/' + str(season_year) + '/' + str(pt_measure_type) + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/leaguedashptstats?' \
              'College=&' \
              'Conference=&' \
              'Country=&' \
              'DateFrom={date_from}&' \
              'DateTo={date_to}&' \
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
        url = url.format(pt_measure_type=pt_measure_type, season_year=season_year, date_from=date_from, date_to=date_to)
        df = json_to_pandas(url, 0)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Gets player details for a team when each player is on the court
def teamplayeronoffdetails(team_id, measure_type='Base', season_year='2016-17', overwrite=True):
    file_path = '../../teamplayeronoffdetails/' + season_year + '/' + measure_type + '/' + str(team_id) + '.csv'
    if (not file_exists(file_path)) or overwrite:
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
        df = json_to_pandas(url, 1)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


# Aggregate on court stats for all teams
def get_all_player_on_data(season_year='2016-17', measure_type='Base', overwrite=True):
    file_path = '../../teamplayeronoffdetails/' + season_year + '/' + measure_type + '/' + 'All.csv'
    if (not file_exists(file_path)) or overwrite:
        team_ids = leaguedashplayerstats(season_year=season_year)['TEAM_ID'].unique()
        df = pd.DataFrame()
        for team_id in team_ids:
            print(team_id)
            df = df.append(teamplayeronoffdetails(team_id, season_year=season_year, measure_type=measure_type))
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


def boxscoretraditionalv2(game_id, season_year='2016-17', overwrite=False):
    if len(str(game_id)) < 10:
        game_id = '00' + str(game_id)
    file_path = '../../data/boxscoretraditionalv2/' + season_year + '/' + str(game_id) + '/' + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/boxscoretraditionalv2?' \
              'EndPeriod=10&' \
              'EndRange=28800&' \
              'GameID={game_id}&' \
              'RangeType=0&' \
              'Season={season_year}&' \
              'SeasonType=Regular+Season&' \
              'StartPeriod=1&StartRange=0'
        url = url.format(game_id=game_id, season_year=season_year)
        df = json_to_pandas(url)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)


def boxscoreadvancedv2(game_id, season_year='2016-17', overwrite=False):
    if len(str(game_id)) < 10:
        game_id = '00' + str(game_id)
    file_path = '../../data/boxscoreadvancedv2/' + season_year + '/' + str(game_id) + '/' + '.csv'
    if (not file_exists(file_path)) or overwrite:
        url = 'http://stats.nba.com/stats/boxscoreadvancedv2?' \
              'EndPeriod=10&' \
              'EndRange=28800&' \
              'GameID={game_id}&' \
              'RangeType=0&' \
              'Season={season_year}&' \
              'SeasonType=Regular+Season&' \
              'StartPeriod=1&StartRange=0'
        url = url.format(game_id=game_id, season_year=season_year)
        df = json_to_pandas(url, index=1)
        df.to_csv(file_path)
        return df
    else:
        return pd.read_csv(file_path)