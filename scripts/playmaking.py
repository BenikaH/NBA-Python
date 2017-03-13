import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

from scripts import data_getters as d


def calculate_23pt_ast_for_players():
    assists = []
    for year in range(2015, 2016):
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
                    'year': year,
                    'two_pt_ast': float(two_pt_assists),
                    'three_pt_ast': float(three_pt_assists),
                    '2points': (2 * two_pt_assists),
                    '3points': (3 * three_pt_assists),
                    'points': ((3 * three_pt_assists) + (2 * two_pt_assists)),
                    'pct_three_pt_ast': pct_three_pt_assists
                })
    assist_df = p.DataFrame(assists).reindex()
    assist_df['total_ast'] = assist_df['two_pt_ast'] + assist_df['three_pt_ast']
    assist_df.fillna(0)
    assist_df = assist_df[(assist_df['three_pt_ast'] < 10000) & (assist_df['games_played'] > 10)]

    assist_df = assist_df[
        ['player_name', '2points', '3points', 'points', 'year', 'games_played', 'total_ast', 'two_pt_ast',
         'three_pt_ast', 'pct_three_pt_ast']]
    # assist_df = assist_df[assist_df['year'].str.contains('Chris Paul') == True].sort_values(by='year')
    assist_df = assist_df.sort_values(by='three_pt_ast', ascending=False).head(50)
    d.print_reddit_table(
        assist_df,
        ['player_name', 'games_played', 'total_ast', 'two_pt_ast', 'three_pt_ast', 'pct_three_pt_ast', 'points'])
    return assist_df


def plot_bar_chart_23pt_ast_for_players(df):
    # df = df.sort_values(by='total_ast', ascending=False)
    # df = df.head(10)
    trace1 = go.Bar(
        x=df['player_name'],
        y=df['2points'],
        name='Points on 2pt assists'
    )
    trace2 = go.Bar(
        x=df['player_name'],
        y=df['3points'],
        name='Points on 3pt assists'
    )

    layout = go.Layout(
        barmode='stack',
        annotations=[
            dict(x=xi, y=yi,
                 text=str(yi),
                 xanchor='center',
                 yanchor='bottom',
                 showarrow=False,
                 ) for xi, yi in zip(df['player_name'].append(df['player_name']), (df['3points'].append(df['points'])).round(1))]
    )

    fig = go.Figure(data=[trace2, trace1], layout=layout)
    # py.plot(fig, filename='assists-stacked-bar')


plot_bar_chart_23pt_ast_for_players(calculate_23pt_ast_for_players())
