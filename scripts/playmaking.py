import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

from scripts import data_getters as d


def calculate_23pt_ast_for_players():
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


def plot_bar_chart_23pt_ast_for_players(df):
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
    py.plot(fig, filename='assists-stacked-bar')


def classify_shots_by_zone_and_year():
    years_by_distance = []
    for y in range(1996, 2017):
        year_string = d.get_year_string(y)
        shots = p.read_csv('../data/merged_shot_pbp/' + year_string + '.csv')
        num_shots = len(shots)

        shots_by_distance = {}
        for dist in range(0, 29):
            shots_by_distance[dist] = round(len(shots[shots.SHOT_DISTANCE == dist]) * 100 / num_shots, 2)

        print(year_string + ' ||| ' + str(shots_by_distance))
        shots_by_distance['Year'] = str(y)
        years_by_distance.append(shots_by_distance)

    full_df = p.DataFrame(years_by_distance)
    d.print_reddit_table(full_df, full_df.columns)
    return full_df


def plot_shot_zones():
    shots = classify_shots_by_zone_and_year()
    zone_traces = []
    total = 0
    for zone in shots.columns:
        if zone != 'Year':
            zone_traces.append(go.Scatter(
                x=shots.Year,
                y=shots[zone] + total,
                name=zone,
                mode='lines',
                line=dict(width=0.5),
                fill='tonexty'
            ))
            total += shots[zone]
    py.plot(zone_traces, filename='shot_zones_by_year')


plot_shot_zones()