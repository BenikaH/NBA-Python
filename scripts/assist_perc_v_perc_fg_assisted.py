from data_getters import get_stat_csv, PlayerOrTeam, MeasureTypes, PerModes, SeasonTypes, get_year_string
import pandas as pd
import os.path
import plotly.graph_objs as go
import plotly.plotly as py


def get_stats(overwrite):
    if not os.path.exists('../data/apvpfa'):
        os.makedirs('../data/apvpfa')
        print('MAKING DIRECTORY')
    file_path = '../data/apvpfa/data.csv'
    if (not os.path.isfile(file_path)) or overwrite:
        return_df = pd.DataFrame(columns=['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'AST_PCT', 'YEAR'])
        for year in range(1996, 2016):
            print(year)
            adv_stat_df = get_stat_csv(PlayerOrTeam.P, MeasureTypes.ADV, PerModes.TOTAL, get_year_string(year),
                                       SeasonTypes.REG)
            adv_stat_df = adv_stat_df[adv_stat_df.GP >= 50]
            adv_stat_df = adv_stat_df[adv_stat_df.MIN >= 25]
            adv_stat_df = adv_stat_df[adv_stat_df.USG_PCT >= .25]
            adv_stat_df = adv_stat_df[['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'AST_PCT']]
            shooting_stat_df = get_stat_csv(PlayerOrTeam.P, MeasureTypes.SCORING, PerModes.TOTAL, get_year_string(year),
                                            SeasonTypes.REG)
            shooting_stat_df = shooting_stat_df[['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME', 'PCT_AST_FGM']]
            yearly_df = pd.merge(adv_stat_df, shooting_stat_df, how='left', on=['PLAYER_ID', 'TEAM_ID', 'PLAYER_NAME'])
            yearly_df['YEAR'] = " " + get_year_string(year)
            return_df = return_df.append(yearly_df, ignore_index=True)
        return_df.to_csv(file_path)
        return_df['DISPLAY'] = return_df['PLAYER_NAME'] + return_df['YEAR']
        return return_df
    else:
        return pd.read_csv(file_path)


def plot_data(plot_df):
    trace0 = go.Scatter(
        x=plot_df['AST_PCT'],
        y=plot_df['PCT_AST_FGM'],
        mode='markers',
        text=plot_df['DISPLAY']
    )
    layout = go.Layout(
        title='Assist Percentage vs. Percentage of Field Goals Assisted',
        hovermode='closest',
        xaxis=dict(title='Assist Percentage'),
        yaxis=dict(title='Percentage of Field Goals Assisted')
    )
    fig = go.Figure(data=[trace0], layout=layout)
    url = py.plot(fig, filename='Assist vs Assisted')


df = get_stats(True)
plot_data(df)
