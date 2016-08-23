import os.path

import numpy as np
import pandas as pd
import plotly.plotly as py
from plotly.tools import FigureFactory as FF

from data_getters import PlayerOrTeam, PerModes, SeasonTypes, MeasureTypes
from data_getters import get_stat_csv, get_player_passing_dashboard, get_year_string


def build_csv(overwrite):
    if not os.path.exists('../data/p2p_assists/'):
        os.makedirs('../data/p2p_assists')
        print('MAKING DIRECTORY : ' + './data/p2p_assists')
    file_path = '../data/p2p_assists/passing.csv'
    if (not os.path.isfile(file_path)) or overwrite:
        passing_df = pd.DataFrame(
            columns=['Year', 'Receiver_Id', 'Receiver_Name', 'Passer_Id', 'Passer_Name', 'Frequency', 'Pass',
                     'Assists'])
        for year in range(2013, 2016):
            base_df = get_stat_csv(PlayerOrTeam.P, MeasureTypes.BASE, PerModes.TOTAL, get_year_string(year),
                                   SeasonTypes.REG)
            for index, receiver in base_df.iterrows():
                print(receiver.PLAYER_NAME)
                player_passing_df = get_player_passing_dashboard(receiver.PLAYER_ID, get_year_string(year))
                if player_passing_df is not None:
                    for index2, passer in player_passing_df.iterrows():
                        row = [year, passer.PLAYER_ID, passer.PLAYER_NAME_LAST_FIRST, passer.PASS_TEAMMATE_PLAYER_ID,
                               passer.PASS_FROM, passer.FREQUENCY, passer.PASS, passer.AST]
                        passing_df = passing_df.append(pd.Series(row, index=passing_df.columns), ignore_index=True)
        passing_df = passing_df.sort_values(by='Assists', ascending=False)
        passing_df.to_csv(file_path)
        return passing_df
    else:
        return pd.read_csv(file_path)


def build_plotly_table(plotly_df):
    plotly_df = plotly_df[['Passer_Name', 'Receiver_Name', 'Assists']]
    plotly_df = plotly_df.sort_values(by='Assists', ascending=False)
    plotly_df = plotly_df.head(25)
    plotly_df.columns = ['Passer', 'Receiver', 'Assists']
    plotly_df = plotly_df.as_matrix()
    plotly_df = np.insert(plotly_df, 0, np.array(('Passer', 'Receiver', 'Assists')), 0)

    table = FF.create_table(plotly_df)
    py.iplot(table, filename='assist_pairs')


df = build_csv(True)
