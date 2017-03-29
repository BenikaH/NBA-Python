from scripts.util import data_getters as d
import pandas as p


def calculate_bad_pass_turnovers(player_df, player_id):
    player_df = player_df[player_df.PLAYER1_ID == player_id]
    player_df = player_df.fillna('0')
    return len(player_df[player_df.HOMEDESCRIPTION.str.contains('Bad Pass Turnover')]) + len(
        player_df[player_df.VISITORDESCRIPTION.str.contains('Bad Pass Turnover')]) + len(
        player_df[player_df.NEUTRALDESCRIPTION.str.contains('Bad Pass Turnover')])


def compile_stats_for_year(year='2016-17'):
    player_ids = d.leaguedashplayerstats(overwrite=False).sort_values(by='AST', ascending=False).head(
        27).PLAYER_ID.unique()
    shots_df = p.read_csv('../../data/merged_shot_pbp/' + year + '.csv')
    tracking_df = d.leaguedashpstats("Passing", overwrite=False)

    assist_stats = []
    for ix, player_id in enumerate(player_ids):
        game_ids = d.playergamelog(player_id=str(player_id), season_year=year, overwrite=False).Game_ID.unique()

        player_pbp_df = p.DataFrame()
        for jx, game_id in enumerate(game_ids):
            player_pbp_df = player_pbp_df.append(d.playbyplayv2(game_id=game_id, year=year, overwrite=False))

        bad_pass = calculate_bad_pass_turnovers(player_pbp_df, player_id)

        player_ast_df = shots_df[shots_df.PLAYER2_ID == player_id]

        games_played = len(player_ast_df.GAME_ID.unique())
        two_point_ast = len(player_ast_df[player_ast_df.SHOT_TYPE == '2PT Field Goal'])
        three_point_ast = len(player_ast_df[player_ast_df.SHOT_TYPE == '3PT Field Goal'])

        total_pass = tracking_df[tracking_df.PLAYER_ID == player_id].iloc[0].PASSES_MADE

        player_name = player_ast_df.iloc[0].PLAYER2_NAME

        print(player_name)

        assist_stats.append({
            'Player': player_name,
            'Bad Passes': bad_pass,
            '2PT Ast': two_point_ast,
            '3PT Ast': three_point_ast,
            'Total Ast': two_point_ast + three_point_ast,
            'Total Passes': total_pass,
            'Ast to Pass': float(total_pass) / (two_point_ast + three_point_ast),
            'Points From Ast': (2 * two_point_ast) + (3 * three_point_ast),
            'Ast To Bad Pass': float(two_point_ast + three_point_ast) / bad_pass,
            'Points To Bad Pass': float((2 * two_point_ast) + (3 * three_point_ast)) / bad_pass,
            'Total Pass To Bad Pass': float(total_pass) / bad_pass
        })

    return p.DataFrame(assist_stats).sort_values(by='Total Ast', ascending=False)


df = compile_stats_for_year()
# d.print_reddit_table(df,
#                      ['Player', 'Total Ast', '2PT Ast', '3PT Ast', 'Points From Ast', 'Bad Passes', 'Ast To Bad Pass',
#                       'Points To Bad Pass'])
d.print_reddit_table(df, ['Player', 'Total Ast', 'Total Passes', 'Bad Passes', 'Total Pass To Bad Pass', 'Ast to Pass'])
print(df[['Ast to Pass', 'Total Pass To Bad Pass']].corr())
