import pandas as p
import data_getters as d


def merge_shot_and_pbp_year(season_year):
    print('MERGING SHOT AND PBP DATA FOR ' + str(season_year))
    # get shot data
    shot_log = d.shotchartdetail(year=season_year, overwrite=False)

    # get game id's from game log
    game_log = d.leaguegamelog(year=season_year, overwrite=True)
    game_ids = game_log.GAME_ID.unique()

    # get play by play data
    # append play by play from each game to play by play data frame
    play_by_play = p.DataFrame()
    for ix, game_id in enumerate(game_ids):
        print(str(ix) + ' / ' + str(len(game_ids)) + ' games done')
        if len(str(game_id)) < 10:
            game_id = '00' + str(game_id)
        play_by_play = play_by_play.append(d.playbyplayv2(str(game_id), year=year, overwrite=False))

    # merge shot and play by play data
    return p.merge(shot_log, play_by_play, left_on=['GAME_ID', 'GAME_EVENT_ID'], right_on=['GAME_ID', 'EVENTNUM'])


for year in range(1996, 2017):
    year = d.get_year_string(year)
    merge_shot_and_pbp_year(year).to_csv('../data/merged_shot_pbp/' + str(year) + '.csv')
