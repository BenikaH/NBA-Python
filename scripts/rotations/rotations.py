import pandas as p
from scripts import data_getters as d
import numpy as np


# takes in pctimestring and period columns and returns a combined column which represents seconds into the game
def convert_time(time, quarter):
    quarter.map(int)
    mins = time.map(lambda x: x.split(':')[0]).map(int)
    seconds = time.map(lambda x: x.split(':')[1]).map(int)
    return ((quarter - 1) * 12 * 60) + ((12 * 60) - (mins * 60) - seconds)


def get_half_time_starters(pbp_df):
    pbp_df = pbp_df[pbp_df.PERIOD == 3]
    pbp_df = pbp_df[pbp_df.HOMEDESCRIPTION.str.contains('SUB') == True]
    return pbp_df.PLAYER1_ID.unique()[0:5]


def generate_rotations_from_play_by_play(game_id, season='2016-17'):
    play_by_play = p.read_csv('../../data/playbyplayv2/' + season + '/' + game_id + '.csv')
    play_by_play['TIME'] = convert_time(play_by_play.PCTIMESTRING, play_by_play.PERIOD)

    game_id = play_by_play.iloc[0].GAME_ID
    if len(str(game_id)) < 10:
        game_id = '00' + str(game_id)

    home_team_id = play_by_play[play_by_play.HOMEDESCRIPTION.notnull()].iloc[0].PLAYER1_TEAM_ID
    away_team_id = play_by_play[play_by_play.VISITORDESCRIPTION.notnull()].iloc[0].PLAYER1_TEAM_ID

    box_score = d.boxscoretraditionalv2(game_id).fillna('')

    box_score = box_score[box_score.START_POSITION != '']
    home_lineup = box_score[box_score.TEAM_ID == home_team_id].PLAYER_ID.unique()
    away_lineup = box_score[box_score.TEAM_ID == away_team_id].PLAYER_ID.unique()

    play_by_play.HOMEDESCRIPTION.fillna(' ')
    home_subs = play_by_play[play_by_play.HOMEDESCRIPTION.str.contains('SUB') == True]

    home_lineups = [dict(player_ids=home_lineup, start_time=0)]
    i=0
    half_time = False
    for ix, sub in home_subs.iterrows():
        if sub.PERIOD == 3 and not half_time:
            home_lineup = get_half_time_starters(pbp_df=play_by_play)
            half_time = True

        player_out = sub.PLAYER1_ID
        player_in = sub.PLAYER2_ID

        index = np.argwhere(home_lineup == player_out)
        home_lineup = np.delete(home_lineup, index)
        home_lineup = np.append(home_lineup, player_in)

        home_lineups[i]['end_time'] = sub.TIME
        home_lineups.append(dict(player_ids=home_lineup, start_time=sub.TIME))
        i += 1
    home_lineups[i]['end_time'] = 4 * 12 * 60

    2+2


generate_rotations_from_play_by_play('0021600880')