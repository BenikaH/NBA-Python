import pandas as p

from scripts.util import data_getters as d


def calc_pts_per_potential_ast_for_year(year='2016-17'):
    df = d.leaguedashpstats('Passing', season_year=year)
    df['PTS_PER_POTENTIAL_AST'] = df['AST_PTS_CREATED'].map(float) / df['POTENTIAL_AST'].map(float)
    df = df.sort_values(by='POTENTIAL_AST', ascending=False)
    df['YEAR'] = year
    df = df[['PLAYER_NAME', 'YEAR', 'POTENTIAL_AST', 'AST_PTS_CREATED', 'PTS_PER_POTENTIAL_AST']]
>>>>>>> c49fc973d87141191719ca081ac76e9d44aabb8c:scripts/playmaking/ast_plus/tracking.py
    return df


def calc_pts_per_potential_ast_for_year_range(start_year=2013, end_year=2017):
    df = p.DataFrame()
    for year in range(start_year, end_year):
        year_string = d.get_year_string(year)
        print('====================================')
        print('Getting Points Per Potential Assist For ' + year_string)
        print('====================================')
        df = df.append(calc_pts_per_potential_ast_for_year(year_string))
    df = df.sort_values(by='POTENTIAL_AST', ascending=False)
    return df


calc_pts_per_potential_ast_for_year()