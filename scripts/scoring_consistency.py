import pandas as pd
import plotly.graph_objs as go
import os.path

from data_getters import j2p, get_stat_csv, get_player_game_logs


def get_yearly_data(overwrite_file):

    file_path = '../data/scoring_consistency/top_scorers.csv'

    if not os.path.exists('../data/scoring_consistency'):
        print("MAKING DIRECTORY!")
        os.makedirs('../data/scoring_consistency')
    else:
        print("DIRECTORY EXISTS!")

    if os.path.isfile(file_path) and not overwrite_file:
        print("ALREADY HAVE TOP SCORERS FILE!")
        return pd.read_csv(file_path)
    else:
        print("NEED TO GET TOP SCORERS FILE")
        data_df = pd.DataFrame()
        for year in range(1996, 2016):
            year_string = str(year) + "-" + str(year + 1)[2:4]
            print("GETTING STATS FOR: " + year_string)

            year_df = get_stat_csv("player", "Base", "PerGame", year_string, "Regular+Season")

            year_df = year_df[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GP', 'PTS']]
            year_df["YEAR"] = year_string
            year_df["YEAR_DISPLAY"] = " '" + str(year+1)[2:4]
            year_df = year_df.loc[year_df["GP"] >= 50]
            year_df = year_df.loc[year_df["PTS"] >= 25]
            last_names = [x[1] for x in year_df["PLAYER_NAME"].str.split().tolist()]
            year_df["DISPLAY"] = last_names + year_df["YEAR_DISPLAY"]

            if year == 1996:
                data_df = year_df
            else:
                data_df = data_df.append(year_df)

        data_df.to_csv(file_path)
        return data_df


def make_traces():
    func_traces = []
    yearly_stats_df = pd.read_csv("../data/scoring_consistency/top_scorers.csv")
    var_df = pd.DataFrame(columns=['PLAYER_NAME', 'PP36', 'VAR', 'STD_DEV'])

    for index, player in yearly_stats_df.iterrows():
        player_log_df = get_player_game_logs(player.YEAR, "Regular+Season", player.PLAYER_NAME, player.PLAYER_ID)

        player_log_df = player_log_df[player_log_df.MIN >= 25]
        player_log_df['PP36'] = (player_log_df['PTS'] / player_log_df['MIN']) * 36

        point_list = player_log_df["PP36"].values
        trace = go.Box(
            y=point_list,
            name=player.DISPLAY
        )
        func_traces.append(trace)

        var_row = [player.DISPLAY, player_log_df['PP36'].mean(), player_log_df['PP36'].var(), player_log_df['PP36'].std()]
        var_df = var_df.append(pd.Series(var_row, index=['DISPLAY', 'PP36', 'VAR', 'STD_DEV']), ignore_index=True)

    func_traces.sort(key=lambda x: x.y.var())

    var_df.to_csv("../data/scoring_consistency/scoring_variance.csv")

    return func_traces


get_yearly_data(0)
traces = make_traces()
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

t1 = traces[0:10]
t2 = traces[-10:]
traces = t1 + t2

#fig = go.Figure(data=traces, layout=layout)
#url = py.plot(fig, file_name="Variance Scorers")
