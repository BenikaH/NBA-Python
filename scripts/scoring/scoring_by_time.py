import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py


# takes in pctimestring and period columns and returns a combined column which represents seconds into the game
def convert_time(time, quarter):
    quarter.map(int)
    mins = time.map(lambda x: x.split(':')[0]).map(int)
    seconds = time.map(lambda x: x.split(':')[1]).map(int)
    return ((quarter - 1) * 12 * 60) + ((12 * 60) - (mins * 60) - seconds)


# read from csv and format data
def get_data(data_year='2016-17'):
    data_df = p.read_csv('../../data/merged_shot_pbp/' + data_year + '.csv')

    data_df['TIME'] = convert_time(data_df.PCTIMESTRING, data_df.PERIOD)
    data_df = data_df[['TIME', 'PLAYER1_ID', 'PLAYER1_NAME', 'PLAYER1_TEAM_ID']]
    data_df = data_df[data_df.TIME < (4 * 12 * 60)]

    return data_df


def plot_box_chart(team_id):
    data_df = get_data()
    data_df = data_df[data_df.PLAYER1_TEAM_ID == team_id]
    layout = go.Layout(
        title='Scoring By Time',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )
    traces = []
    for player in data_df.PLAYER1_ID.unique():
        player_df = data_df[data_df.PLAYER1_ID == player]
        traces.append(go.Box(
            y=player_df.TIME,
            name=player_df.iloc[0].PLAYER1_NAME,
            whiskerwidth=0,
            boxpoints='all',
            boxmean=True,
            jitter=1,
            pointpos=0,
            line=dict(
                width=0
            )))

    fig = go.Figure(data=traces, layout=layout)
    py.plot(fig, filename="Scoring By Time")


plot_box_chart(1610612740)
