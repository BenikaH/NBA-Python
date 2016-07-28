import pandas as pd
from data_getters import synergy_play_types
import os.path


def consolidate_synergy_files(file_overwrite):
    file_path = './data/Team_data/Synergy/Consolidated_offensive_2015-16.csv'
    if not os.path.exists(file_path) or file_overwrite:
        consolidate_df = pd.DataFrame()
        for st in synergy_play_types:
            file_path = './data/Team_data/Synergy/' + st + '_offensive_2015-16.csv'
            st_df = pd.read_csv(file_path)
            2+2

consolidate_synergy_files(1)
