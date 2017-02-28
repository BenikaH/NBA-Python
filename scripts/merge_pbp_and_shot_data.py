import pandas as p

from scripts import data_getters as d


def merge_shot_and_pbp_year(season_year, shot_ow=False, log_ow=False, pbp_ow=False):
    print('MERGING SHOT AND PBP DATA FOR ' + str(season_year))
    # get shot data
    shot_log = d.shotchartdetail(year=season_year, overwrite=shot_ow)

    # get game id's from game log
    game_log = d.leaguegamelog(year=season_year, overwrite=log_ow)
    game_ids = game_log.GAME_ID.unique()

    # get play by play data
    # append play by play from each game to play by play data frame
    play_by_play = p.DataFrame()
    for ix, game_id in enumerate(game_ids):
        print(str(ix) + ' / ' + str(len(game_ids)) + ' games done')
        if len(str(game_id)) < 10:
            game_id = '00' + str(game_id)
        play_by_play = play_by_play.append(d.playbyplayv2(str(game_id), year=year, overwrite=pbp_ow))

    # merge shot and play by play data
    return p.merge(shot_log, play_by_play, left_on=['GAME_ID', 'GAME_EVENT_ID', 'PERIOD'],
                   right_on=['GAME_ID', 'EVENTNUM', 'PERIOD'])


def data_is_correct(test_year):
    shot_log = d.shotchartdetail(year=d.get_year_string(test_year), overwrite=False)
    data_df = p.read_csv('../data/merged_shot_pbp/' + d.get_year_string(test_year) + '.csv')
    data_shots = len(data_df)
    actual_shots = len(shot_log)
    print(d.get_year_string(test_year) + ' : ' + str(data_shots/actual_shots))
    return data_shots / actual_shots > .9


def test_data():
    years_with_error = []
    for data_year in range(1996, 2017):
        if not data_is_correct(data_year):
            years_with_error.append(d.get_year_string(data_year))
    print(years_with_error)
    return years_with_error


# for year in range(2012, 2013):
#     year = d.get_year_string(year)
#     merge_shot_and_pbp_year(year).to_csv('../data/merged_shot_pbp/' + str(year) + '.csv')

years_to_update = test_data()
for year in years_to_update:
    merge_shot_and_pbp_year(year, pbp_ow=False)
    data_is_correct(d.get_year_string(year))