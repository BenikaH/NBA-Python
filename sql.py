import MySQLdb
import data_getters as data
import pandas as pd

db = MySQLdb.connect(host='localhost', user='root', passwd='1qw2SQL3er4', db='nbadb')
cur = db.cursor()

df = pd.DataFrame()

for year in range(1996, 2016):
    base_df = data.get_general_stats(data.PlayerOrTeam.P, data.MeasureTypes.BASE, data.PerModes.TOTAL, year,
                                     data.SeasonTypes.REG)
    base_df['YEAR'] = data.get_year_string(year)
    base_df = base_df[
        ['PLAYER_ID', 'TEAM_ID', 'YEAR', 'AGE', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN', 'AST', 'BLK', 'DREB',
         'OREB', 'FGA', 'FGM', 'FG3A', 'FG3M', 'FTA', 'FTM', 'PTS', 'STL', 'PLUS_MINUS', 'W', 'L', 'PF', 'PFD']]
    df = df.append(base_df)

df.to_sql(name='nba_playerbasestats', con=db, flavor='mysql', if_exists='replace')
