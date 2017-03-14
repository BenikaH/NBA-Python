import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

from scripts.util import data_getters as d

season_year = '2016-17'
consistency_data_file_path = './data/consistency/' + season_year + '_variance.csv'
consistency_data_player_log_path = './data/consistency/{player_id}_' + season_year + '.csv'
consistency_data_overwrite = True


def get_consistency_data():
    if (not d.file_exists(consistency_data_file_path)) or consistency_data_overwrite:
        base_stats_df = d.leaguedashplayerstats()
        base_stats_df = base_stats_df[base_stats_df['GP'] > 25]
        base_stats_df['PPG'] = base_stats_df['PTS'] / base_stats_df['GP']
        base_stats_df = base_stats_df.sort_values(by='PPG', ascending=False).head(20)
        print(base_stats_df[['PLAYER_NAME']])

        data_df = p.DataFrame(
            columns=['PLAYER_ID', 'PLAYER_NAME', 'PP36', 'PP36_STD', 'PP36_STD / MEAN', 'PP36_VAR', 'TS', 'TS_STD',
                     'TS_VAR'])
        top_scoring_player_ids = base_stats_df['PLAYER_ID'].unique()
        for player_id in top_scoring_player_ids:
            player_game_log_file_path = consistency_data_player_log_path.format(player_id=player_id)
            if (not d.file_exists(player_game_log_file_path)) or consistency_data_overwrite:
                player_game_log_df = d.playergamelog(player_id)
                # player_game_log_df = player_game_log_df[player_game_log_df['MIN'] > 20]
                # player_game_log_df = player_game_log_df[player_game_log_df['PTS'] > 1]

                player_game_log_df['PP36'] = (player_game_log_df['PTS'] / player_game_log_df['MIN']) * 36

                player_game_log_df['TSA'] = player_game_log_df['FGA'] + (0.44 * player_game_log_df['FTA'])
                player_game_log_df['TS'] = (player_game_log_df['PTS'] / (2 * player_game_log_df['TSA'])) * 100

                player_game_log_df.to_csv(player_game_log_file_path)
            else:
                player_game_log_df = p.read_csv(player_game_log_file_path)

            pp36 = player_game_log_df['PP36'].mean()
            pp36_std = player_game_log_df['PP36'].std()
            pp36_var = player_game_log_df['PP36'].var()

            ts = player_game_log_df['TS'].mean()
            ts_std = player_game_log_df['TS'].std()
            ts_var = player_game_log_df['TS'].var()

            player_name = base_stats_df[base_stats_df['PLAYER_ID'] == player_id].iloc[0]['PLAYER_NAME']

            row = [player_id, player_name, pp36, pp36_std, pp36_std / pp36, pp36_var, ts, ts_std, ts_var]
            data_df = data_df.append(p.Series(row, index=data_df.columns), ignore_index=True)

        data_df.to_csv(consistency_data_file_path)
        return data_df
    else:
        return p.read_csv(consistency_data_file_path)


def generate_consistency_plots(data_df):
    layout = go.Layout(
        title='Scoring Consistency',
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

    pp36_traces = []
    ts_traces = []
    for ix, player in data_df.iterrows():
        player_file_path = consistency_data_player_log_path.format(player_id=int(player.PLAYER_ID))
        player_df = p.read_csv(player_file_path)
        player_pp36_trace = go.Box(
            y=player_df['PP36'],
            name=player.PLAYER_NAME,
            whiskerwidth=0,
            boxpoints='all',
            boxmean=True,
            jitter=1,
            pointpos=0,
            line=dict(
                width=0
            )
        )
        pp36_traces.append(player_pp36_trace)
        player_ts_trace = go.Box(
            y=player_df['TS'],
            name=player.PLAYER_NAME,
            whiskerwidth=0,
            boxpoints='all',
            boxmean=True,
            jitter=1,
            pointpos=0,
            line=dict(
                width=0
            )
        )
        ts_traces.append(player_ts_trace)

    pp36_traces.sort(key=lambda x: x.y.std())
    layout.title = 'PP36 Consistency'
    fig = go.Figure(data=pp36_traces, layout=layout)
    url = py.plot(fig, filename="PP36 Consistency")

    layout.title = 'PP36 Consistency (Mean Adjusted)'
    pp36_traces.sort(key=lambda x: x.y.std() / x.y.mean())
    fig = go.Figure(data=pp36_traces, layout=layout)
    url = py.plot(fig, filename="PP36 Consistency (Mean Adjusted)")

    layout.title = 'TS Consistency'
    ts_traces.sort(key=lambda x: x.y.std())
    fig = go.Figure(data=ts_traces, layout=layout)
    url = py.plot(fig, filename="TS Consistency")
