import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

import data_getters as d
from numpy import array

season_year = '2016'
offensive_or_defensive = 'offensive'
synergy_data_file_path = './data/synergy/' + season_year + '.csv'
synergy_data_overwrite = False
consistency_data_file_path = './data/consistency/' + season_year + '_variance.csv'
consistency_data_player_log_path = './data/consistency/{player_id}_' + season_year + '.csv'
consistency_data_overwrite = True


def get_synergy_data():
    if (not d.file_exists(filepath=synergy_data_file_path)) or synergy_data_overwrite:
        print('Getting Synergy Data from stats.nba.com API....')
        data_df = d.allsynergy(season_year=season_year,
                               offensive_or_defensive=offensive_or_defensive)
        data_df.to_csv(synergy_data_file_path, encoding='utf-8')
        return data_df
    else:
        print('Getting Synergy Data from ' + synergy_data_file_path + '....')
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
        print(row.PLAYER_LAST_NAME)
        layout = go.Layout(
            title=row.PLAYER_FIRST_NAME + ' ' + row.PLAYER_LAST_NAME + ' Expected Scoring',
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


def streaky_shooters(window_sizes, num_players):
    streaky_shooters_df = p.DataFrame(columns=['Player Name'])
    for window_size in window_sizes:
        # Get merged shot and pbp data
        shots_df = p.read_csv('../data/merged_shot_pbp/2016-17.csv')

        # Gets 3 points attempt leader ids, filter for players with more than 20 games played
        general_stats_df = d.leaguedashplayerstats(overwrite=False)
        general_stats_df = general_stats_df[general_stats_df['GP'] > 20]
        general_stats_df = general_stats_df.sort_values(by='FG3A', ascending=False).head(num_players)
        player_ids = general_stats_df['PLAYER_ID'].unique()

        # Arrays to hold plot traces
        scatter_traces = []
        box_traces = []

        # Arrays to hold player names and standard deviation for df
        player_names = []
        player_stds = []

        # Enumerate player ids, filter shot df by player_id; use filtered df to create trace for player
        for player_id in player_ids:
            # Filter df
            player_shots_df = shots_df[shots_df['PLAYER1_ID'] == player_id]
            player_shots_df = player_shots_df[player_shots_df['SHOT_TYPE'] == '3PT Field Goal']
            # Multiply shot made flag so that rolling average represents percentage
            player_shots_df['SHOT_MADE_FLAG'] *= 100
            print(player_shots_df.columns)
            print(player_shots_df.head(50))

            # Get chart attributes
            player_name = player_shots_df.iloc[1].PLAYER_NAME
            # Calculate Array of rollings averages across a given window size of shots
            player_means = player_shots_df['SHOT_MADE_FLAG'].rolling(window=window_size, center=False).mean().values
            player_means = player_means[(window_size - 1):]
            # Array used to represent shot number (chronologically)
            shot_nums = range(0, len(player_means) - (window_size - 1))

            # Append to plot traces
            scatter_traces.append(
                go.Scatter(
                    x=shot_nums,
                    y=player_means,
                    mode='lines+markers',
                    name=player_name)
            )
            box_traces.append(
                go.Box(
                    y=player_means,
                    name=player_name,
                    whiskerwidth=0,
                    boxpoints='all',
                    boxmean=True,
                    jitter=1,
                    pointpos=0,
                    line=dict(
                        width=0
                    )
                )
            )

            # Append to df arrays
            player_names.append(player_name)
            player_stds.append(player_means.std())

        # Sort Box Traces by Standard Deviation of the player rolling means
        box_traces = sorted(box_traces, key=lambda x: x.y.std())

        # Plot Traces
        layout = dict(
            title='Streaky Shooters (Window = ' + str(window_size) + ')'
        )
        # py.iplot(scatter_traces, layout=layout, filename='W' + str(window_size) + ' Streaky Shooters Scatter')

        # py.iplot(box_traces, layout=layout, filename='W: ' + str(window_size) + ' Streaky Shooters Box')

        # Add column for window size to overall streak shooters df
        streaky_shooters_window_df = p.DataFrame()
        streaky_shooters_window_df['Player Name'] = player_names
        player_stds = array(player_stds)
        player_stds = (player_stds - player_stds.mean()) / player_stds.std()
        streaky_shooters_window_df['W' + str(window_size) + ' STD'] = player_stds
        streaky_shooters_df = streaky_shooters_df.merge(streaky_shooters_window_df, on=['Player Name'], how='outer')

    d.print_reddit_table(streaky_shooters_df, streaky_shooters_df.columns)
    player_names = streaky_shooters_df['Player Name']
    del streaky_shooters_df['Player Name']
    heat_map_data = [go.Heatmap(z=streaky_shooters_df.values.tolist(), y=player_names, x=streaky_shooters_df.columns,
                                colorscale='Viridis')]

    # py.iplot(heat_map_data, filename='W:' + str(window_sizes) + ' Heat Map')


streaky_shooters([10, 25, 50, 75, 100], 20)
