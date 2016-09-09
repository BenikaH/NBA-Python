import pandas as pd
import shot_charts as charts

import data_getters as data


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


def merge_pbp_and_shot_data():
    year = 2015
    game_ids = get_season_game_ids(year)
    full_year_merged_df = pd.DataFrame()
    for i, game_id in enumerate(game_ids):
        print(i)
        pbp_df = data.get_pbp_data(game_id, data.get_year_string(year), data.SeasonTypes.REG, overwrite=False)
        pbp_df = pbp_df[
            ['GAME_ID', 'EVENTNUM', 'PERIOD', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION',
             'VISITORDESCRIPTION',
             'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ID',
             'PLAYER3_ID',
             'PLAYER3_NAME', 'PLAYER3_TEAM_ID']]

        shot_df = data.get_shot_data(game_id=game_id, overwrite=False)
        shot_df = shot_df[
            ['ACTION_TYPE', 'EVENT_TYPE', 'GAME_EVENT_ID', 'GAME_ID', 'LOC_X', 'LOC_Y', 'SHOT_DISTANCE',
             'SHOT_MADE_FLAG',
             'SHOT_TYPE', 'SHOT_ZONE_AREA', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_RANGE']]

        merge_df = pd.merge(pbp_df, shot_df, left_on=['GAME_ID', 'EVENTNUM'], right_on=['GAME_ID', 'GAME_EVENT_ID'],
                            how='inner')
        full_year_merged_df = full_year_merged_df.append(merge_df)
        full_year_merged_df.to_csv('merge.csv')


def chart_assists():
    df = pd.read_csv('merge.csv')
    players_df = data.get_general_stats(data.PlayerOrTeam.P, data.MeasureTypes.BASE, data.PerModes.TOTAL, 2015,
                                        data.SeasonTypes.REG)
    players_df = players_df.sort_values(by=['AST'], ascending=False).head(30)
    for i, player in players_df.iterrows():
        print(player.PLAYER_ID, player.PLAYER_NAME)
        player_df = df[df['PLAYER2_ID'] == player.PLAYER_ID]
        # charts.make_matplot_scatter_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
        #                                       data.SeasonTypes.REG, 'assist')
        charts.make_matplot_hexbin_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
                                              data.SeasonTypes.REG, 'assist')
        # charts.make_matplot_kde_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
        #                                   data.SeasonTypes.REG, 'assist')


def chart_blocks():
    df = pd.read_csv('merge.csv')
    players_df = data.get_general_stats(data.PlayerOrTeam.P, data.MeasureTypes.BASE, data.PerModes.TOTAL, 2015,
                                        data.SeasonTypes.REG)
    players_df = players_df.sort_values(by=['BLK'], ascending=False).head(30)
    for i, player in players_df.iterrows():
        print(player.PLAYER_ID, player.PLAYER_NAME)
        player_df = df[df['PLAYER3_ID'] == player.PLAYER_ID]
        charts.make_matplot_scatter_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
                                               data.SeasonTypes.REG, 'blocks')
        charts.make_matplot_hexbin_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
                                              data.SeasonTypes.REG, 'blocks')
        charts.make_matplot_kde_shot_chart(player_df, player.PLAYER_NAME, player.PLAYER_ID, 2015,
                                           data.SeasonTypes.REG, 'blocks')


chart_assists()
# chart_blocks()
