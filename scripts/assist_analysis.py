import data_getters as d
import pandas as p
import plotly.plotly as py
import plotly.graph_objs as go


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
            pct_three_pt_assists = float(three_pt_assists) / float((three_pt_assists + two_pt_assists))
            games_played = len(player_df['GAME_ID'].unique())
            assists.append({
                'player_name': str(player_name) + ' ' + d.get_year_string(year),
                'games_played': games_played,
                'two_pt_ast': float(two_pt_assists) / games_played,
                'three_pt_ast': float(three_pt_assists) / games_played,
                'pct_three_pt_ast': pct_three_pt_assists
            })
    assist_df = p.DataFrame(assists).reindex()
    assist_df['total_ast'] = assist_df['two_pt_ast'] + assist_df['three_pt_ast']
    assist_df.fillna(0)
    assist_df = assist_df.sort_values(by='three_pt_ast', ascending=False)
    assist_df = assist_df[
        (assist_df['total_ast'] < 20) & (assist_df['total_ast'] > 5) & (assist_df['games_played'] > 20)]
    assist_df = assist_df[
        ['player_name', 'games_played', 'total_ast', 'two_pt_ast', 'three_pt_ast', 'pct_three_pt_ast']].sort_values(
        by='three_pt_ast', ascending=False).head(500)
    d.print_reddit_table(assist_df, assist_df.columns)
    three_pt_assist_df = assist_df[assist_df['three_pt_ast'] > assist_df['two_pt_ast']]
    d.print_reddit_table(three_pt_assist_df, three_pt_assist_df.columns)
    return assist_df


def plot_bar_chart_of_assists(df):
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

    fig = go.Figure(data=[trace1, trace2], layout=layout)
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


calc_2_3_assists()
