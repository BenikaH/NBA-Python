import data_getters as d
import pandas as p

import plotly.graph_objs as go
import plotly.plotly as py

season_year = '2016'
offensive_or_defensive = 'offensive'
synergy_data_file_path = './data/synergy/' + season_year + '.csv'
synergy_data_overwrite = False
consistency_data_file_path = './data/consistency/' + season_year + '_variance.csv'
consistency_data_player_log_path = './data/consistency/{player_id}_' + season_year + '.csv'
consistency_data_overwrite = False


def get_synergy_data():
    if (not d.create_directories_and_check_for_file(filepath=synergy_data_file_path)) or synergy_data_overwrite:
        print('Don\'t have stats yet, getting from stats.nba.com API....')
        data_df = d.get_combined_synergy_stats_for_players(season_year=season_year,
                                                           offensive_or_defensive=offensive_or_defensive)
        data_df.to_csv(synergy_data_file_path, encoding='utf-8')
        return data_df
    else:
        return p.read_csv(synergy_data_file_path, encoding='utf-8')


def calc_points_above_exp(data_df):
    data_df['Total_PTS_ABOVE_EXP'] = 0
    data_df['Total_EXP_PTS'] = 0
    for play_type in d.synergy_play_types:
        data_df[play_type + '_PTS_ABOVE_EXP'] = data_df[play_type + '_POSS'] * data_df[play_type + '_PPP_ABOVE_MEAN']
        data_df['Total_PTS_ABOVE_EXP'] += data_df[play_type + '_POSS'] * data_df[play_type + '_PPP_ABOVE_MEAN']
        data_df['Total_EXP_PTS'] += data_df[play_type + '_EXP_PTS']
    data_df['Total_EXP_PPP'] = data_df['Total_EXP_PTS'] / data_df['Total_POSS']
    return data_df


def graph_player_pts_above_exp(data_df):
    for ix, row in data_df.iterrows():
        layout = go.Layout(
            title=row.PLAYER_FIRST_NAME + ' ' + row.PLAYER_LAST_NAME + 'EXP_SCORING',
            barmode='stack',
            paper_bgcolor='rgba(245, 246, 249, 1)',
            plot_bgcolor='rgba(245, 246, 249, 1)',
            showlegend=False
        )
        traces = []
        y_data = []
        for play_type in d.synergy_play_types:
            y_data.append(row[play_type + '_PTS_ABOVE_EXP'])
        traces.append(go.Bar(
            x=d.synergy_play_types,
            y=y_data,
            name=row.PLAYER_FIRST_NAME + ' ' + row.PLAYER_LAST_NAME,
            marker=dict(
                color=y_data
            )
        ))
        fig = go.Figure(data=traces, layout=layout)
        url = py.plot(fig, filename=row.PLAYER_FIRST_NAME + ' ' + row.PLAYER_LAST_NAME + 'EXP_SCORING')


def get_consistency_data():
    if (not d.create_directories_and_check_for_file(consistency_data_file_path)) or consistency_data_overwrite:
        base_stats_df = d.get_general_stats()
        base_stats_df = base_stats_df[base_stats_df['GP'] > 25]
        base_stats_df = base_stats_df.sort_values(by='PTS', ascending=False).head(50)

        data_df = p.DataFrame(
            columns=['PLAYER_ID', 'PLAYER_NAME', 'PP36', 'PP36_STD', 'PP36_VAR', 'TS', 'TS_STD', 'TS_VAR'])
        top_scoring_player_ids = base_stats_df['PLAYER_ID'].unique()
        for player_id in top_scoring_player_ids:
            player_game_log_file_path = consistency_data_player_log_path.format(player_id=player_id)
            if (not d.create_directories_and_check_for_file(player_game_log_file_path)) or consistency_data_overwrite:
                player_game_log_df = d.get_game_logs_for_player(player_id)
                player_game_log_df = player_game_log_df[player_game_log_df['MIN'] > 20]

                player_game_log_df['PP36'] = (player_game_log_df['PTS'] / player_game_log_df['MIN']) * 36

                player_game_log_df['TSA'] = player_game_log_df['FGA'] + (0.44 * player_game_log_df['FTA'])
                player_game_log_df['TS'] = player_game_log_df['PTS'] / (2 * player_game_log_df['TSA'])

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

            row = [player_id, player_name, pp36, pp36_std, pp36_var, ts, ts_std, ts_var]
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
            name=player.PLAYER_NAME
        )
        pp36_traces.append(player_pp36_trace)
        player_ts_trace = go.Box(
            y=player_df['TS'],
            name=player.PLAYER_NAME
        )

    pp36_traces.sort(key=lambda x: x.y.std())
    layout.title = 'PP36 Variance'
    fig = go.Figure(data=pp36_traces, layout=layout)
    url = py.plot(fig, filename="PP36 Variance")

    layout.title = 'PP36 Variance over Mean'
    pp36_traces.sort(key=lambda x: x.y.std() / x.y.mean())
    fig = go.Figure(data=pp36_traces, layout=layout)
    url = py.plot(fig, filename="PP36 Variance over Mean")

    layout.title = 'TS Variance'
    ts_traces.sort(key=lambda x: x.y.std())
    fig = go.Figure(data=pp36_traces, layout=layout)
    url = py.plot(fig, filename="TS Variance")


# df = get_synergy_data()
# df = calc_points_above_exp(df).sort_values(by='Total_PTS_ABOVE_EXP', ascending=False).head(10)
# d.print_reddit_table(df=df, columns=['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'Total_PTS_ABOVE_EXP', 'Total_PPP',
#                                     'Total_EXP_PPP'])
# graph_player_pts_above_exp(df)

df = get_consistency_data()
generate_consistency_plots(df)
