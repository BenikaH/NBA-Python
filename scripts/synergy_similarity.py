import pandas as pd
import os.path
from data_getters import get_synergy_stats
from data_getters import get_stat_csv
from data_getters import synergy_play_types


def get_data(overwrite):
    dir_path = "../data/player_data/synergy_similarity"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = dir_path + "/synergy_freqs.csv"
    if (not os.path.isfile(file_path)) or overwrite:
        data_df = get_stat_csv("player", "Base", "Totals", "2015-16", "Regular+Season")
        data_df = data_df[["PLAYER_ID", "PLAYER_NAME"]]
        for index, stype in enumerate(synergy_play_types):
            stype_df = get_synergy_stats("player", stype, "offensive")
            stype_df = stype_df[["PlayerIDSID", "Time"]]
            stype_df.columns = ["PLAYER_ID", stype + "_Frequency"]
            data_df = data_df.merge(stype_df, on="PLAYER_ID", how="left")
        data_df = data_df.fillna(0)
        data_df.to_csv(file_path)
        return data_df
    else:
        return pd.read_csv(file_path)


def calc_sim_scores(in_df):
    print(len(in_df))
    sim_score_df = pd.DataFrame(columns=["Player1", "Player2", "SimScore"])
    sim_score_by_player_df = pd.DataFrame(columns=["MainPlayer", "MostSimilar", "SimScore"])
    for index, player in in_df.iterrows():
        player1Name = player.PLAYER_NAME
        player1Freqs = player.tolist()[3:]
        highestSimScore = 0
        for index2, player2 in in_df.iterrows():
            player2Name = player2.PLAYER_NAME
            player2Freqs = player2.tolist()[3:]
            simscore = 100
            for index3, freq in enumerate(player1Freqs):
                simscore -= abs(player1Freqs[index3] - player2Freqs[index3])
            if player1Name != player2Name:
                if simscore > highestSimScore:
                    highestSimScore = simscore
                    playerRow = [player1Name, player2Name, simscore]
                row = [player1Name, player2Name, simscore]
                sim_score_df = sim_score_df.append(pd.Series(row, index=sim_score_df.columns), ignore_index=True)
            if highestSimScore == 0:
                playerRow=[player1Name, "None", "N/A"]
        sim_score_by_player_df = sim_score_by_player_df.append(
            pd.Series(playerRow, index=sim_score_by_player_df.columns), ignore_index=True)
    sim_score_df = sim_score_df.sort_values(by="SimScore", ascending=False)
    sim_score_df = sim_score_df.iloc[::2, :]
    sim_score_df.to_csv("../data/player_data/synergy_similarity/sim_scores_small.csv")
    sim_score_by_player_df.to_csv("../data/player_data/synergy_similarity/sim_scores_by_player_small.csv")


df = get_data(True)
