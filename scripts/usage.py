import pandas as p

from scripts.util import data_getters as d


def get_usage_data(date_to='', date_from=''):
    totals_df = d.leaguedashplayerstats(measure_type='Base', per_mode='Totals', date_to=date_to, date_from=date_from)
    totals_df = totals_df[['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'GP', 'MIN', 'PTS', 'FGA', 'FTA', 'AST', 'TOV']]
    totals_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'GP', 'MIN', 'TOTAL_PTS', 'TOTAL_FGA', 'TOTAL_FTA',
                         'TOTAL_AST', 'TOTAL_TOV']

    per_100_df = d.leaguedashplayerstats(measure_type='Base', per_mode='Per100Possessions', date_to=date_to,
                                         date_from=date_from)
    per_100_df = per_100_df[['PLAYER_ID', 'TEAM_ID', 'PTS', 'FGA', 'FTA', 'AST', 'TOV']]
    per_100_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PER_POSS_PTS', 'PER_POS_FGA', 'PER_POSS_FTA', 'PER_POSS_AST',
                          'PER_POSS_TOV']

    passing_df = d.leaguedashpstats(pt_measure_type='Passing', overwrite=True, date_from=date_from, date_to=date_to)
    passing_df = passing_df[['PLAYER_ID', 'TEAM_ID', 'POTENTIAL_AST']]

    possession_df = d.leaguedashpstats(pt_measure_type='Possessions', overwrite=True, date_from=date_from, date_to=date_to)
    possession_df = possession_df[['PLAYER_ID', 'TEAM_ID', 'TIME_OF_POSS']]

    usage_df = p.merge(totals_df, per_100_df, on=['PLAYER_ID', 'TEAM_ID'])
    usage_df = usage_df.merge(passing_df, on=['PLAYER_ID', 'TEAM_ID'])
    usage_df = usage_df.merge(possession_df, on=['PLAYER_ID', 'TEAM_ID'])
    usage_df['POSS'] = (usage_df['TOTAL_PTS'] / usage_df['PER_POSS_PTS']) * 100

    usage_df['TOTAL_TSA'] = usage_df['TOTAL_FGA'] + (usage_df['TOTAL_FTA'] * 0.44)
    usage_df['PER_POSS_TSA'] = (usage_df['TOTAL_TSA'] / usage_df['POSS']) * 100
    usage_df['PER_POSS_AST'] = (usage_df['POTENTIAL_AST'] / usage_df['POSS']) * 100
    usage_df['TIME_OF_POSS_PCT'] = (usage_df['TIME_OF_POSS'] / usage_df['MIN']) * 100

    usage_df['USG'] = usage_df['PER_POSS_TSA'] + usage_df['PER_POSS_AST'] + usage_df['PER_POSS_TOV']
    usage_df = usage_df.sort_values(by='USG', ascending=False)
    usage_df = usage_df[['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'USG', 'PER_POSS_TSA', 'PER_POSS_AST', 'PER_POSS_TOV', 'TIME_OF_POSS_PCT']]
    return usage_df


before_df = get_usage_data(date_to='02/22/2017')
before_df = before_df[before_df['PLAYER_NAME'].isin(['Anthony Davis', 'DeMarcus Cousins', 'Jrue Holiday'])]
d.print_reddit_table(before_df, ['PLAYER_NAME', 'USG', 'PER_POSS_TSA', 'PER_POSS_AST', 'PER_POSS_TOV', 'TIME_OF_POSS_PCT'])
before_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'BEF_USG', 'BEF_TSA', 'BEF_AST', 'BEF_TOV', 'BEF_TOP_PCT']

after_df = get_usage_data(date_from='02/22/2017')
after_df = after_df[after_df['PLAYER_NAME'].isin(['Anthony Davis', 'DeMarcus Cousins', 'Jrue Holiday'])]
d.print_reddit_table(after_df, ['PLAYER_NAME', 'USG', 'PER_POSS_TSA', 'PER_POSS_AST', 'PER_POSS_TOV'])
after_df.columns = ['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'AFT_USG', 'AFT_TSA', 'AFT_AST', 'AFT_TOV', 'AFT_TOP_PCT']

diff_df = p.merge(before_df, after_df, on=['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME'])
diff_df['DIFF_USG'] = -diff_df['BEF_USG'] + diff_df['AFT_USG']
diff_df['DIFF_TSA'] = -diff_df['BEF_TSA'] + diff_df['AFT_TSA']
diff_df['DIFF_AST'] = -diff_df['BEF_AST'] + diff_df['AFT_AST']
diff_df['DIFF_TOV'] = -diff_df['BEF_TOV'] + diff_df['AFT_TOV']
diff_df['DIFF_TOP_PCT'] = -diff_df['BEF_TOP_PCT'] + diff_df['AFT_TOP_PCT']
d.print_reddit_table(diff_df, ['PLAYER_NAME', 'DIFF_USG', 'DIFF_TSA', 'DIFF_AST', 'DIFF_TOV', 'DIFF_TOP_PCT'])