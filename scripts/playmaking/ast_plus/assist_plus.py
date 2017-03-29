import pandas as p

from scripts.util import data_getters as d

shot_zones = ['Restricted Area', 'Mid-Range', 'In The Paint (Non-RA)', 'Above the Break 3', 'Left Corner 3',
              'Right Corner 3']


def calculate_efficiency_by_zone(year):
    df = p.read_csv('../../../data/merged_shot_pbp/' + year + '.csv')
    efficiencies = {}
    for ix, sz in enumerate(shot_zones):
        sz_df = df[df.SHOT_ZONE_BASIC == sz]
        points = 3 if '3' in sz else 2
        shots_made = (float(len(sz_df[sz_df.SHOT_MADE_FLAG == 1])))
        shots_attempted = float(len(sz_df))
        points_per_shot = round((shots_made / shots_attempted) * points, 2)
        efficiencies[sz] = points_per_shot
    return efficiencies


def print_reddit_tables_for_ast_plus(print_df, num_players=10, sort_column='ast_per_game'):
    print_df = print_df.sort_values(by=sort_column, ascending=False).head(num_players)
    d.print_reddit_table(print_df,
                         ['name', 'Restricted Area %', 'Mid-Range %', 'In The Paint (Non-RA) %', 'Above the Break 3 %',
                          'Right Corner 3 %', 'Morey %', 'Morey Factor'])


def calculate_assist_plus_for_year(year='2016-17'):
    shots_df = p.read_csv('../../../data/merged_shot_pbp/' + year + '.csv')
    zone_efficiencies = calculate_efficiency_by_zone(year)
    print(zone_efficiencies)
    player_ids = shots_df.PLAYER2_ID.unique()
    num_players = len(player_ids)
    assist_details = []

    for ix, player_id in enumerate(player_ids):
        if player_id != 0:
            player_ast_df = shots_df[shots_df.PLAYER2_ID == player_id]

            player_name = player_ast_df.iloc[0].PLAYER2_NAME
            games_played = len(player_ast_df.GAME_ID.unique())
            total_ast = len(player_ast_df)

            if float(total_ast) / games_played > 4:
                print('Getting Assist+ For ' + player_name + ' (' + str(ix) + '/' + str(num_players) + ')')

                player_assist_details = {
                    'PLAYER_NAME': player_name,
                    'YEAR': year,
                    'GP': games_played,
                    'TOTAL_AST': total_ast,
                    'AST+': 0
                }

                for jx, shot_zone in enumerate(shot_zones):
                    zone_assists = float(len(player_ast_df[player_ast_df.SHOT_ZONE_BASIC == shot_zone]))
                    player_assist_details[shot_zone] = zone_assists
                    player_assist_details[shot_zone + ' %'] = round((zone_assists / total_ast) * 100, 2)
                    player_assist_details['AST+'] += player_assist_details[shot_zone] * zone_efficiencies[shot_zone]

                assist_details.append(player_assist_details)

    df = p.DataFrame(assist_details).reindex()
    df['ast_per_game'] = df['total_assists'] / df['games']

    df['Corner 3'] = df['Right Corner 3'] + df['Left Corner 3']
    df['Corner 3 %'] = df['Right Corner 3 %'] + df['Left Corner 3 %']
    df['Morey %'] = df['Restricted Area %'] + df['Corner 3 %'] + df['Above the Break 3 %']
    df['Morey Factor'] = df['ast_plus'] / df['total_assists']

    df = df.sort_values(by='ast_per_game', ascending=False)

    return df


def calc_ast_plus_for_year_range(start_year=1996, end_year=2017):
    df = p.DataFrame()
    for year in range(start_year, end_year):
        year_string = d.get_year_string(year)
        print('====================================')
        print('Getting Assist+ For ' + year_string)
        print('====================================')
        df = df.append(calculate_assist_plus_for_year(year_string))
    return df


calculate_assist_plus_for_year()