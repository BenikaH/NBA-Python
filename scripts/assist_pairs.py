import data_getters as d
import pandas as p

base_df = d.get_general_stats()
base_df['AST_PER_GAME'] = base_df['AST'] / base_df['GP']
base_df = base_df[base_df['GP'] >= 20]
base_df = base_df.sort_values(by='AST_PER_GAME', ascending=False)

ast_df = base_df[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'MIN', 'AST']]
fgm_df = base_df[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'MIN', 'FGM']]

assist_pair_df = p.DataFrame()
for player_id in base_df.head(10)['PLAYER_ID'].unique():
    player_df = d.get_player_passes(player_id)
    assist_pair_df = assist_pair_df.append(player_df)

assist_pair_df = assist_pair_df[['PLAYER_ID', 'PLAYER_NAME_LAST_FIRST', 'PASS_TEAMMATE_PLAYER_ID', 'PASS_TO', 'AST']]
assist_pair_df.columns = ['PASSER_ID', 'PASSER_NAME', 'SHOOTER_ID', 'SHOOTER_NAME', 'AST']

