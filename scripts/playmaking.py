import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py
import data_getters as d

shot_zones = ['Restricted Area', 'Mid-Range', 'In The Paint (Non-RA)', 'Above the Break 3', 'Left Corner 3',
              'Right Corner 3']


def calculate_efficiency_by_zone(year):
    df = p.read_csv('../data/merged_shot_pbp/' + year + '.csv')
    efficiencies = {}
    for ix, sz in enumerate(shot_zones):
        sz_df = df[df.SHOT_ZONE_BASIC == sz]
        points = 3 if '3' in sz else 2
        shots_made = (float(len(sz_df[sz_df.SHOT_MADE_FLAG == 1])))
        shots_attempted = float(len(sz_df))
        points_per_shot = round((shots_made / shots_attempted) * points, 2)
        efficiencies[sz] = points_per_shot
    return efficiencies


def print_reddit_tables_for_ast_plus(print_df, num_players=10, sort_column='ast_per_game'):
    print_df = print_df.sort_values(by=sort_column, ascending=False).head(num_players)
    d.print_reddit_table(print_df,
                         ['name', 'Restricted Area %', 'Mid-Range %', 'In The Paint (Non-RA) %', 'Above the Break 3 %',
                          'Left Corner 3 %', 'Right Corner 3 %'])

    d.print_reddit_table(print_df,
                         ['name', 'ast_per_game', 'ast_plus_per_game', 'ast_plus_per_ast'])


def calculate_assist_plus_for_year(year):
    shots_df = p.read_csv('../data/merged_shot_pbp/' + year + '.csv')
    zone_efficiencies = calculate_efficiency_by_zone(year)
    player_ids = shots_df.PLAYER2_ID.unique()
    assist_details = []

    for ix, player_id in enumerate(player_ids):
        if player_id != 0:
            player_df = shots_df[shots_df.PLAYER2_ID == player_id]

            total_assists = float(len(player_df))
            player_assist_details = {
                'name': player_df.iloc[0].PLAYER2_NAME,
                'year': year,
                'games': len(player_df.GAME_ID.unique()),
                'total_assists': total_assists,
                'ast_plus': 0
            }

            for jx, shot_zone in enumerate(shot_zones):
                zone_assists = float(len(player_df[player_df.SHOT_ZONE_BASIC == shot_zone]))
                player_assist_details[shot_zone] = zone_assists
                player_assist_details[shot_zone + ' %'] = round((zone_assists / total_assists) * 100, 2)
                player_assist_details['ast_plus'] += player_assist_details[shot_zone] * zone_efficiencies[shot_zone]

            assist_details.append(player_assist_details)

    df = p.DataFrame(assist_details).reindex()
    df['ast_plus_per_game'] = df['ast_plus'] / df['games']
    df['ast_plus_per_ast'] = df['ast_plus'] / df['total_assists']
    df['ast_per_game'] = df['total_assists'] / df['games']
    df = df.sort_values(by='ast_per_game', ascending=False)

    return df


def calculate_assist_plus_for_year_range(start_year=1996, end_year=2017):
    df = p.DataFrame()
    for year in range(start_year, end_year):
        year_string = d.get_year_string(year)
        print(year_string)
        df = df.append(calculate_assist_plus_for_year(year_string))
    print_reddit_tables_for_ast_plus(df, num_players=50)


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
