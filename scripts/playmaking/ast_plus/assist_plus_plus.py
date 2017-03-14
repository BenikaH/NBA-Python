import pandas as p
from scripts.util.data_getters import get_year_string


def calc_ast_plus_plus_for_year(year='2016-17'):
    shots_df = p.read_csv('../../../data/merged_shot_pbp/' + year + '.csv')
    player_ids = shots_df.PLAYER2_ID.unique()
    num_players = len(player_ids)
    assist_details = []

    for ix, player_id in enumerate(player_ids):
        if player_id != 0:
            player_ast_df = shots_df[shots_df.PLAYER2_ID == player_id]

            total_ast = len(player_ast_df)
            player_name = player_ast_df.iloc[0].PLAYER2_NAME
            games_played = len(player_ast_df.GAME_ID.unique())

            if float(total_ast) / games_played > 4:
                print('Getting Assist++ For ' + player_name + ' (' + str(ix) + '/' + str(num_players) + ')')

                player_assist_details = {
                    'PLAYER_NAME': player_name,
                    'YEAR': year,
                    'GP': games_played,
                    'TOTAL_AST': total_ast,
                    'AST++': 0
                }

                for jx, shot in player_ast_df.iterrows():
                    shot_df = shots_df[shots_df.PLAYER1_ID == shot.PLAYER1_ID]
                    shot_df = shot_df[shot_df.SHOT_ZONE_BASIC == shot.SHOT_ZONE_BASIC]
                    made_shots = len(shot_df[shot_df.SHOT_MADE_FLAG == 1])
                    total_shots = len(shot_df)
                    shot_value = 3 if '3' in shot.SHOT_ZONE_BASIC else 2
                    player_assist_details['AST++'] += (float(made_shots) / total_shots) * shot_value

                player_assist_details['AST++_EFF'] = player_assist_details['AST++'] / player_assist_details['TOTAL_AST']
                assist_details.append(player_assist_details)

    ast_df = p.DataFrame(assist_details).sort_values(by='TOTAL_AST', ascending=False)
    return ast_df


def calc_ast_plus_plus_for_year_range(start_year=1996, end_year=2017):
    ast_df = p.DataFrame()
    for year in range(start_year, end_year):
        year_string = get_year_string(year)
        print('====================================')
        print('Getting Assist++ For ' + year_string)
        print('====================================')
        ast_df = ast_df.append(calc_ast_plus_plus_for_year(year_string))
    return ast_df
