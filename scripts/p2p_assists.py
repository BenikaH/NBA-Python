from data_getters import get_stat_csv, get_player_passing_dashboard, get_year_string
from data_getters import PlayerOrTeam, PerModes, SeasonTypes, MeasureTypes
import pandas as pd
import os.path
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
import plotly.tools as tls
import numpy as np
py.sign_in('fenerty64', '5l3888x5bv')


def build_csv(overwrite):
    if not os.path.exists('../data/p2p_assists/'):
        os.makedirs('../data/p2p_assists')
        print('MAKING DIRECTORY : ' + './data/p2p_assists')
    file_path = '../data/p2p_assists/passing.csv'
    if (not os.path.isfile(file_path)) or overwrite:
        base_df = get_stat_csv(PlayerOrTeam.P, MeasureTypes.BASE, PerModes.TOTAL, get_year_string(2015), SeasonTypes.REG)
        passing_df = pd.DataFrame(
            columns=['Receiver_Id', 'Receiver_Name', 'Passer_Id', 'Passer_Name', 'Frequency', 'Pass', 'Assists'])
        for index, receiver in base_df.iterrows():
            print(receiver.PLAYER_NAME)
            player_passing_df = get_player_passing_dashboard(receiver.PLAYER_ID, get_year_string(2015))
            for index2, passer in player_passing_df.iterrows():
                row = [passer.PLAYER_ID, passer.PLAYER_NAME_LAST_FIRST, passer.PASS_TEAMMATE_PLAYER_ID, passer.PASS_FROM,
                       passer.FREQUENCY, passer.PASS, passer.AST]
                passing_df = passing_df.append(pd.Series(row, index=passing_df.columns), ignore_index=True)
        passing_df.to_csv(file_path)
        return passing_df
    else:
        return pd.read_csv(file_path)


df = build_csv(False)
df = df[['Passer_Name', 'Receiver_Name', 'Assists']]
df = df.sort_values(by='Assists', ascending=False)
df = df.head(25)
df.columns = ['Passer', 'Receiver', 'Assists']
df = df.as_matrix()
df = np.insert(df, 0, np.array(('Passer', 'Receiver', 'Assists')), 0)

table = FF.create_table(df)
py.iplot(table, filename='assist_pairs')
