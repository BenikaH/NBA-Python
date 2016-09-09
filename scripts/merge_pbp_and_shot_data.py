import data_getters as data
import pandas as pd


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

year = 2015
game_ids = get_season_game_ids(year)
full_year_merged_df = pd.DataFrame()
for i, game_id in enumerate(game_ids):
    print(i)
    pbp_df = data.get_pbp_data(game_id, data.get_year_string(year), data.SeasonTypes.REG, overwrite=False)
    pbp_df = pbp_df[
        ['GAME_ID', 'EVENTNUM', 'PERIOD', 'PCTIMESTRING', 'HOMEDESCRIPTION', 'NEUTRALDESCRIPTION', 'VISITORDESCRIPTION',
         'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ID', 'PLAYER3_ID',
         'PLAYER3_NAME', 'PLAYER3_TEAM_ID']]

    shot_df = data.get_shot_data(game_id=game_id, overwrite=False)
    shot_df = shot_df[
        ['ACTION_TYPE', 'EVENT_TYPE', 'GAME_EVENT_ID', 'GAME_ID', 'LOC_X', 'LOC_Y', 'SHOT_DISTANCE', 'SHOT_MADE_FLAG',
         'SHOT_TYPE', 'SHOT_ZONE_AREA', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_RANGE']]

    merge_df = pd.merge(pbp_df, shot_df, left_on=['GAME_ID', 'EVENTNUM'], right_on=['GAME_ID', 'GAME_EVENT_ID'],
                        how='inner')
    full_year_merged_df = full_year_merged_df.append(merge_df)
    full_year_merged_df.to_csv('merge.csv')

