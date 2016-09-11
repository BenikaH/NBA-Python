import pandas as pd
import shot_charts as charts
import matplotlib.pyplot as plt
import data_getters as data
import operator


def get_season_game_ids(season_year):
    url = 'http://stats.nba.com/stats/leaguegamelog?' \
          'Counter=1000&' \
          'DateFrom=&' \
          'DateTo=&' \
          'Direction=DESC&' \
          'LeagueID=00&' \
          'PlayerOrTeam=T&' \
          'Season={seasonYear}&' \
          'SeasonType=Regular+Season&' \
          'Sorter=PTS'
    url = url.format(seasonYear=data.get_year_string(season_year))
    func_df = data.json_to_pandas(url, 0)
    return func_df['GAME_ID'].unique()


def merge_pbp_and_shot_data(year):
    file_path = '../data/merged_shot_pbp/' + str(year) + '.csv'
    if not data.create_directories_and_check_for_file(file_path):
        game_ids = get_season_game_ids(year)
        full_year_merged_df = pd.DataFrame()

        shot_df = data.get_shot_data(overwrite=False, season_year=year)
        shot_df = shot_df[
            ['ACTION_TYPE', 'EVENT_TYPE', 'GAME_EVENT_ID', 'GAME_ID', 'LOC_X', 'LOC_Y', 'SHOT_DISTANCE',
             'SHOT_MADE_FLAG',
             'SHOT_TYPE', 'SHOT_ZONE_AREA', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_RANGE']]

        for i, game_id in enumerate(game_ids):
            print(i, game_id)
            pbp_df = data.get_pbp_data(game_id, data.get_year_string(year), data.SeasonTypes.REG, overwrite=False)
            try:
                pbp_df = pbp_df[
                    ['GAME_ID', 'EVENTNUM', 'PERIOD', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION',
                     'VISITORDESCRIPTION', 'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID', 'PLAYER2_ID',
                     'PLAYER2_NAME', 'PLAYER2_TEAM_ID', 'PLAYER3_ID', 'PLAYER3_NAME', 'PLAYER3_TEAM_ID']]

                merge_df = pd.merge(pbp_df, shot_df, left_on=['GAME_ID', 'EVENTNUM'],
                                    right_on=['GAME_ID', 'GAME_EVENT_ID'],
                                    how='inner')
            except KeyError:
                print("KEY ERROR")

        full_year_merged_df = full_year_merged_df.append(merge_df)
        full_year_merged_df.to_csv('../data/merged_shot_pbp/' + str(year) + '.csv')
        return full_year_merged_df

    else:
        return pd.read_csv(file_path)


def chart_assists(data_df, year, num_of_players):
    players_df = data.get_general_stats(data.PlayerOrTeam.P, data.MeasureTypes.BASE, data.PerModes.TOTAL, year,
                                        data.SeasonTypes.REG)
    players_df = players_df.sort_values(by=['AST'], ascending=False).head(num_of_players)
    for i, player in players_df.iterrows():
        player_df = data_df[data_df['PLAYER2_ID'] == player.PLAYER_ID]
        charts.make_matplot_scatter_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                               data.SeasonTypes.REG, 'assist')
        charts.make_matplot_hexbin_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                              data.SeasonTypes.REG, 'assist')
        charts.make_matplot_kde_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                           data.SeasonTypes.REG, 'assist')
        charts.make_histogram(player_df, player.PLAYER_NAME, year, data.SeasonTypes.REG, 'assist')


def chart_blocks(data_df, year, num_of_players):
    players_df = data.get_general_stats(data.PlayerOrTeam.P, data.MeasureTypes.BASE, data.PerModes.TOTAL, year,
                                        data.SeasonTypes.REG)
    players_df = players_df.sort_values(by=['BLK'], ascending=False).head(num_of_players)
    for i, player in players_df.iterrows():
        print(player.PLAYER_ID, player.PLAYER_NAME)
        player_df = data_df[data_df['PLAYER3_ID'] == player.PLAYER_ID]
        charts.make_matplot_scatter_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                               data.SeasonTypes.REG, 'blocks')
        charts.make_matplot_hexbin_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                              data.SeasonTypes.REG, 'blocks')
        charts.make_matplot_kde_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, year,
                                           data.SeasonTypes.REG, 'blocks')
        charts.make_histogram(player_df, player.PLAYER_NAME, year, data.SeasonTypes.REG, 'block')


def get_alley_oop_pairs(data_df):
    alley_oop_df = data_df[data_df['ACTION_TYPE'].isin(['Alley Oop Dunk Shot', 'Alley Oop Layup Shot'])]
    alley_oop_df = alley_oop_df[alley_oop_df['SHOT_MADE_FLAG'] == 1]
    alley_oop_df['Player_Pairs'] = alley_oop_df['PLAYER2_NAME'].map(str) + ' to ' + alley_oop_df['PLAYER1_NAME']
    player_pairs = alley_oop_df['Player_Pairs'].unique()
    pairs = {}
    for i, pair in enumerate(player_pairs):
        pair_df = alley_oop_df[alley_oop_df['Player_Pairs'] == pair]
        num_of_oops = pair_df.shape[0]
        if num_of_oops > 4:
            pairs[pair] = num_of_oops
    pairs = sorted(pairs.items(), key=operator.itemgetter(1), reverse=True)
    for i, pair in enumerate(pairs):
        print(pair[0] + ' | ' + str(pair[1]))


def get_alley_oop_finishers(data_df):
    alley_oop_df = data_df[data_df['ACTION_TYPE'].isin(['Alley Oop Dunk Shot', 'Alley Oop Layup Shot'])]
    alley_oop_df = alley_oop_df[alley_oop_df['SHOT_MADE_FLAG'] == 1]
    players = alley_oop_df['PLAYER1_NAME'].unique()
    pairs = {}
    for i, player in enumerate(players):
        player_df = alley_oop_df[alley_oop_df['PLAYER1_NAME'] == player]
        num_of_oops = player_df.shape[0]
        if num_of_oops > 4:
            pairs[player] = num_of_oops
    pairs = sorted(pairs.items(), key=operator.itemgetter(1), reverse=True)
    for i, pair in enumerate(pairs):
        print(pair[0] + ' | ' + str(pair[1]))


def get_alley_oop_throwers(data_df):
    alley_oop_df = data_df[data_df['ACTION_TYPE'].isin(['Alley Oop Dunk Shot', 'Alley Oop Layup Shot'])]
    alley_oop_df = alley_oop_df[alley_oop_df['SHOT_MADE_FLAG'] == 1]
    players = alley_oop_df['PLAYER2_NAME'].unique()
    pairs = {}
    for i, player in enumerate(players):
        player_df = alley_oop_df[alley_oop_df['PLAYER2_NAME'] == player]
        num_of_oops = player_df.shape[0]
        if num_of_oops > 4:
            pairs[player] = num_of_oops
    pairs = sorted(pairs.items(), key=operator.itemgetter(1), reverse=True)
    for i, pair in enumerate(pairs):
        print(pair[0] + ' | ' + str(pair[1]))


for year in range(1996, 2016):
    merge_pbp_and_shot_data(year)
