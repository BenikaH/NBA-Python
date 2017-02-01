import data_getters as d
import pandas as p
import plotly.plotly as py
import plotly.graph_objs as go

year = '2016-17'


def calc_2_3_assists(df):
    player_ids = df['PLAYER2_ID'].unique()
    assists = {}
    for ix, player_id in enumerate(player_ids):
        player_df = df[df['PLAYER2_ID'] == player_id]
        player_name = player_df.iloc[0]['PLAYER2_NAME']
        two_pt_assists = len(player_df[player_df['SHOT_TYPE'] == '2PT Field Goal'])
        three_pt_assists = len(player_df[player_df['SHOT_TYPE'] == '3PT Field Goal'])
        pct_three_pt_assists = float(three_pt_assists) / float((three_pt_assists + two_pt_assists))
        assists[ix] = {
            'player_name': player_name,
            'two_pt_ast': two_pt_assists,
            'three_pt_ast': three_pt_assists,
            'pct_three_pt_ast': pct_three_pt_assists
        }
    assist_df = p.DataFrame.from_dict(assists, orient='index').reset_index()
    assist_df['total_ast'] = assist_df['two_pt_ast'] + assist_df['three_pt_ast']
    assist_df = assist_df[['player_name', 'total_ast', 'two_pt_ast', 'three_pt_ast', 'pct_three_pt_ast']].sort_values(
        by='total_ast', ascending=False).head(50)
    assist_df.fillna(0)
    assist_df = assist_df[assist_df['total_ast'] < 10000]
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


plot_bar_chart_of_assists(calc_2_3_assists(p.read_csv('../data/merged_shot_pbp/' + year + '.csv')).head(20))
