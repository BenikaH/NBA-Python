import data_getters as d
import pandas as p

years = ['2013-14', '2014-15', '2015-16', '2016-17']

df = p.DataFrame()
for year in years:
    year_df = d.leaguedashplayerstats(season_year=year)[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PTS', 'FGA', 'FTA', 'AST', 'TOV', 'MIN']]
    year_df = year_df.merge(d.leaguedashplayerstats(measure_type='Advanced', season_year=year)[['PLAYER_ID', 'TEAM_ID', 'PACE']], on=['PLAYER_ID', 'TEAM_ID'])
    year_df = year_df.merge(d.leaguedashpstats('Passing', season_year=year)[['PLAYER_ID', 'TEAM_ID', 'PASSES_MADE', 'FT_AST', 'SECONDARY_AST', 'POTENTIAL_AST','AST_PTS_CREATED']], on=['PLAYER_ID', 'TEAM_ID'])
    year_df = year_df.merge(d.leaguedashpstats('Possessions', season_year=year)[['PLAYER_ID', 'TEAM_ID', 'TOUCHES', 'TIME_OF_POSS']], on=['PLAYER_ID', 'TEAM_ID'])
    year_df['YEAR'] = year
    df = df.append(year_df)

df['POSS'] = df['PACE'] * (df['MIN'] / 48)

df = df[df['POSS'] > 1000]

df['SCORING_USG'] = ((df['FGA'] + (0.44 * df['FTA'])) / df['POSS']) * 100
df['PLAYMAKING_USG'] = (df['POTENTIAL_AST'] / df['POSS']) * 100
df['TOV_USG'] = (df['TOV'] / df['POSS']) * 100

df['TOT_USG'] = df['SCORING_USG'] + df['PLAYMAKING_USG'] + df['TOV_USG']
df['TOT_EFF'] = (df['AST_PTS_CREATED'] + df['PTS']) / ((df['TOT_USG'] / 100) * df['POSS'])

df = df.sort_values(by='TOT_USG', ascending=False)

df = df[['PLAYER_NAME', 'YEAR', 'SCORING_USG', 'PLAYMAKING_USG', 'TOV_USG', 'TOT_USG', 'TOT_EFF']]
df.to_csv('true_usage.csv')
