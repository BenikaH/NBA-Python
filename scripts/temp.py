from scripts.util import data_getters as d
import pandas as p

import plotly.plotly as py
import plotly.graph_objs as go


df = p.DataFrame()
for year in range(1996, 2016):
    year_string = d.get_year_string(year)
    regular_df = d.leaguedashteamstats(measure_type='Advanced', season_year=year_string, season_type='Regular+Season',
                                       overwrite=True)[
        ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']]
    playoff_df = d.leaguedashteamstats(measure_type='Advanced', season_year=year_string, season_type='Playoffs',
                                       overwrite=True)[
        ['TEAM_NAME', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']]
    regular_df.columns = ['Team', 'Reg_ORtg', 'Reg_DRtg', 'Reg_NRtg']
    playoff_df.columns = ['Team', 'Post_ORtg', 'Post_DRtg', 'Post_NRtg']
    regular_df['Year'] = year_string
    playoff_df['Year'] = year_string
    merge_df = p.merge(regular_df, playoff_df, on=['Team', 'Year'], how='inner')
    df = df.append(merge_df)

Offense = go.Scatter(
    x=df['Reg_ORtg'],
    y=df['Post_NRtg'],
    name='Offense'
)

Defense = go.Scatter(
    x=df['Reg_DRtg'],
    y=df['Post_NRtg'],
    name='Defense'
)

layout = go.Layout(
    xaxis=dict(title='Regular O/D Rating Season'),
    yaxis=dict(title='Post Net Rating Season')
)

fig = go.Figure(data=[Offense, Defense], layout=layout)
py.plot(fig, filename='Post Season Corr')