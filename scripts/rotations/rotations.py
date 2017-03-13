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

    play_by_play.HOMEDESCRIPTION.fillna(' ')
    home_subs = play_by_play[play_by_play.HOMEDESCRIPTION.str.contains('SUB') == True]
    starters = home_subs.head(5).PLAYER1_NAME

    2+2


generate_rotations_from_play_by_play('0021600880')