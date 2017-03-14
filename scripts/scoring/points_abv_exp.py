import pandas as p
import plotly.graph_objs as go
import plotly.plotly as py

from scripts.util import data_getters as d

season_year = '2016'
offensive_or_defensive = 'offensive'
synergy_data_file_path = './data/synergy/' + season_year + '.csv'
synergy_data_overwrite = False


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
        py.plot(fig, filename=row.PLAYER_FIRST_NAME + ' ' + row.PLAYER_LAST_NAME + 'EXP_SCORING')