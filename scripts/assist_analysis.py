import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

from scripts import data_getters as d


def calc_2_3_assists():
    assists = []
    for year in range(1996, 2017):
        print(d.get_year_string(year))
        year_df = p.read_csv('../data/merged_shot_pbp/' + d.get_year_string(year) + '.csv')
        player_ids = year_df['PLAYER2_ID'].unique()
        for ix, player_id in enumerate(player_ids):
            player_df = year_df[year_df['PLAYER2_ID'] == player_id]
            player_name = player_df.iloc[0]['PLAYER2_NAME']
            two_pt_assists = len(player_df[player_df['SHOT_TYPE'] == '2PT Field Goal'])
            three_pt_assists = len(player_df[player_df['SHOT_TYPE'] == '3PT Field Goal'])
            if three_pt_assists + two_pt_assists > 0:
                pct_three_pt_assists = float(three_pt_assists) / float((three_pt_assists + two_pt_assists))
                games_played = len(player_df['GAME_ID'].unique())
                assists.append({
                    'player_name': str(player_name) + ' ' + d.get_year_string(year),
                    'games_played': games_played,
                    'year': d.get_year_string(year),
                    'two_pt_ast': float(two_pt_assists) / games_played,
                    'three_pt_ast': float(three_pt_assists) / games_played,
                    'pct_three_pt_ast': pct_three_pt_assists
                })
    assist_df = p.DataFrame(assists).reindex()
    assist_df['total_ast'] = assist_df['two_pt_ast'] + assist_df['three_pt_ast']
    assist_df.fillna(0)
    assist_df = assist_df[(assist_df['three_pt_ast'] < 10) & (assist_df['games_played'] > 20)]

    assist_df = assist_df[
        ['player_name', 'year', 'games_played', 'total_ast', 'two_pt_ast', 'three_pt_ast', 'pct_three_pt_ast']]
    d.print_reddit_table(assist_df.sort_values(by='three_pt_ast', ascending=False).head(10),
                         ['player_name', 'total_ast', 'two_pt_ast', 'three_pt_ast', 'pct_three_pt_ast'])
    return assist_df


def plot_bar_chart_of_assists(df):
    df = df[df.year == '2016-17']
    df = df.sort_values(by='total_ast', ascending=False).head(10)
    trace1 = go.Bar(
        x=df['player_name'],
        y=df['two_pt_ast'],
        name='2PT Assists'
    )
    trace2 = go.Bar(
        x=df['player_name'],
        y=df['three_pt_ast'],
        name='3PT Assists'
    )

    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=[trace2, trace1], layout=layout)
    py.iplot(fig, filename='assists-stacked-bar')


def plot_assists_vs_tov():
    df = d.leaguedashplayerstats(per_mode='Per100Possessions')
    df = df[df['GP'] > 20]
    df = df.sort_values(by='AST', ascending=False).head(50)
    # df['AST_VS_TOV'] = df['AST'] / df['TOV']
    # d.print_reddit_table(df, ['PLAYER_NAME', 'AST', 'TOV', 'AST_VS_TOV'])
    trace = go.Scatter(
        x=df['AST'],
        y=df['TOV'],
        text=df['PLAYER_NAME'],
        mode='markers'
    )
    layout = go.Layout(
        yaxis=dict(
            autorange='reversed'
        )
    )
    fig = go.Figure(
        data=[trace],
        layout=layout
    )
    py.iplot(fig, filename='AST_VS_TOV')


def plot_assists_vs_time_of_poss():
    # Get advanced stats (pace, total mins), Tracking passing stats (potential assists)
    passing_df = d.leaguedashpstats(pt_measure_type='Passing', overwrite=False)
    possession_df = d.leaguedashpstats(pt_measure_type='Possessions', overwrite=False)

    df = p.merge(possession_df, passing_df, on=['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME'], how='inner')
    df['FOO'] = df['POTENTIAL_AST'] / (df['TIME_OF_POSS'].map(float) * df['GP_x'].map(float) / 60)
    df = df.sort_values(by=['POTENTIAL_AST'], ascending=False).head(50)
    df = df.sort_values(by=['FOO'], ascending=False)
    d.print_reddit_table(df, ['PLAYER_NAME', 'FOO'])


ast_df = calc_2_3_assists()
# plot_bar_chart_of_assists(ast_df)
