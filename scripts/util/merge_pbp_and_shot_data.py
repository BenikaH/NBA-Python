import pandas as p

from scripts.util import data_getters as d


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
        play_by_play = play_by_play.append(d.playbyplayv2(str(game_id), year=season_year, overwrite=pbp_ow))

    # merge shot and play by play data
    print(shot_log.head(10))
    print(play_by_play.head(10))
    return_df = p.merge(shot_log, play_by_play, left_on=['GAME_ID', 'GAME_EVENT_ID', 'PERIOD'],
                   right_on=['GAME_ID', 'EVENTNUM', 'PERIOD'], how='inner')
    print(len(return_df))
    return_df.to_csv('../data/merged_shot_pbp/' + season_year + '.csv')
    return return_df


def add_missing_games(add_year):
    data_df = p.read_csv('../data/merged_shot_pbp/' + add_year + '.csv')
    game_log = d.leaguegamelog(year=add_year, overwrite=True)
    data_games = data_df.GAME_ID.unique().astype(int)
    actual_games = game_log.GAME_ID.unique().astype(int)
    missing_games = [x for x in actual_games if x not in data_games]
    print(missing_games)
    for ix, game in enumerate(missing_games):
        print("Getting " + str(ix) + " / " + str(len(missing_games)) + " missing games")
        if len(str(game)) < 10:
            game = '00' + str(game)
        df = d.playbyplayv2(str(game), add_year, overwrite=False)
        data_df = data_df.append(df)
    data_df.to_csv('../data/merged_shot_pbp/' + add_year + '.csv')


def data_is_correct(test_year):
    game_log = d.leaguegamelog(year=test_year, overwrite=False)
    shot_log = d.shotchartdetail(year=test_year, overwrite=False)
    data_df = p.read_csv('../data/merged_shot_pbp/' + test_year + '.csv')
    data_games = data_df.GAME_ID.unique().astype(int)
    actual_games = game_log.GAME_ID.unique().astype(int)
    missing_games = [x for x in actual_games if x not in data_games]
    print(test_year + ' : ' + str(len(missing_games)) + ' games missing ||| ' + str(
        len(shot_log) - len(data_df)) + ' shots missing')
    return len(missing_games) < 10


def test_data():
    years_with_error = []
    for data_year in range(1996, 2017):
        if not data_is_correct(d.get_year_string(data_year)):
            years_with_error.append(d.get_year_string(data_year))
    print(years_with_error)
    return years_with_error
