from scripts.playmaking.ast_plus.assist_plus import calc_ast_plus_for_year_range
from scripts.playmaking.ast_plus.assist_plus_plus import calc_ast_plus_plus_for_year_range
from scripts.playmaking.ast_plus.tracking import calc_pts_per_potential_ast_for_year_range
import pandas as p


start_year = 2013
end_year = 2017


def compare_metrics():
    tracking_df = calc_pts_per_potential_ast_for_year_range(start_year, end_year)
    ast_plus_df = calc_ast_plus_for_year_range(start_year, end_year)
    ast_plus_plus_df = calc_ast_plus_plus_for_year_range(start_year, end_year)
    df = p.merge(ast_plus_df, ast_plus_plus_df, on=['PLAYER_NAME', 'YEAR', 'TOTAL_AST'], how='inner')
    df = df.merge(tracking_df, on=['PLAYER_NAME', 'YEAR'], how='inner')

    test_df = df[['PLAYER_NAME', 'YEAR', 'AST+_EFF', 'AST++_EFF', 'PTS_PER_POTENTIAL_AST']]
    test_df['AST++-AST+'] = test_df['AST++_EFF'] - test_df['AST+_EFF']
    test_df['PPPA-AST++'] = test_df['PTS_PER_POTENTIAL_AST'] - df['AST++_EFF']
    return df

compare_metrics()