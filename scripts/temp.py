from scripts.util import data_getters as d
import pandas as p

game_log = d.leaguegamelog(year='2016-17', overwrite=False)
game_log = game_log[game_log.TEAM_ABBREVIATION == 'NOP']
game_ids = game_log.GAME_ID.unique()

adv_log = p.DataFrame()
for ix, game_id in enumerate(game_ids):
    print(str(ix) + '/' + str(len(game_ids)))
    adv_box = d.boxscoreadvancedv2(game_id, season_year='2016-17', overwrite=False)
    adv_box = adv_box[adv_box.TEAM_ABBREVIATION == 'NOP']
    adv_log = adv_log.append(adv_box)

2+2