from data_getters import get_stat_csv, get_sports_vu_stats
import pandas as pd
import os.path
import plotly.graph_objs as go
import plotly.plotly as py


def get_data():
    file_path = '../data/offensive_v_defensive_pace/data.csv'
    if not os.path.exists('../data/offensive_v_defensive_pace'):
        print("MAKING DIRECTORY!")
        os.makedirs('../data/offensive_v_defensive_pace')
    else:
        print("DIRECTORY EXISTS!")
    if os.path.isfile(file_path) and not overwrite_file:
        print("ALREADY HAVE OFFENSIVE AND DEFENSIVE PACE DATA!")
        return pd.read_csv(file_path)
    else:
        print("NEED TO GET OFFNESIVE AND DEFENSIVE PACE DATA!")
        data_df = pd.DataFrame(
            columns=['GP', 'YEAR', 'TEAM_ID', 'TEAM_NAME', 'OFF_TOP', 'DEF_TOP', 'ORTG', 'DRTG', 'PACE'])
        for year in range(2013, 2016):
            season_year = str(year) + "-" + str(year + 1)[2:4]
            print('YEAR => ' + season_year)
            year_df = pd.DataFrame(
                columns=['GP', 'YEAR', 'TEAM_ID', 'TEAM_NAME', 'OFF_TOP', 'DEF_TOP', 'ORTG', 'DRTG', 'PACE'])
            # get advanced team data for each year for ORTG, DRTG, and PACE
            print('GETTING ADVANCED TEAM DATA')
            year_adv_df = get_stat_csv("Team", "Advanced", "Totals", season_year, "Regular+Season")
            # get sportsVU possession data for each year for Offensive Time of Possession
            print('GETTING SPORTSVU POSSESSION DATA')
            year_svu_df = get_sports_vu_stats("Team", "Possessions", "Totals", season_year, "Regular+Season", '0')
            # defensive possession time, not given explicitly but you can pass opponent id as a parameter and then sum
            # the possession time of teams playing against each team to calculate defensive possession time
            for index, team in year_adv_df.iterrows():
                print('GETTING POSSESSION TIMES FOR ' + team.TEAM_NAME)
                opp_id = team.TEAM_ID
                offensive_top = year_svu_df.loc[year_svu_df['TEAM_ID'] == opp_id]['TIME_OF_POSS'].values[0]
                print('OFFENSIVE TIME OF POSSESSION => ' + str(offensive_top))
                games = year_svu_df.loc[year_svu_df['TEAM_ID'] == opp_id]['GP'].values[0]
                team_year_svu_df = get_sports_vu_stats("Team", "Possessions", "Totals", season_year, "Regular+Season",
                                                       opp_id)
                defensive_top = team_year_svu_df['TIME_OF_POSS'].sum()
                print('DEFENSIVE TIME OF POSSESSION =>' + str(defensive_top))
                year_df = year_df.append(pd.Series(
                    [games, season_year, opp_id, team.TEAM_NAME, offensive_top, defensive_top, team.OFF_RATING,
                     team.DEF_RATING, team.PACE],
                    index=['GP', 'YEAR', 'TEAM_ID', 'TEAM_NAME', 'OFF_TOP', 'DEF_TOP', 'ORTG', 'DRTG', 'PACE']),
                    ignore_index=True)
            data_df = data_df.append(year_df)
        data_df['TOTAL_POSSESSIONS'] = data_df['PACE'] * data_df['GP']
        data_df.to_csv(file_path)
        return data_df


def generate_plot():
    plot_df = pd.read_csv('../data/offensive_v_defensive_pace/data.csv')
    traces = []
    layouts = []
    traces[0] = go.Scatter(
        x=plot_df['TOTAL_POSSESSIONS'] / plot_df['OFF_TOP'],
        y=plot_df['ORTG'],
        text=plot_df['TEAM_NAME']
    )
    layouts[0] = go.Layout(
        title='Offensive Pace vs Offensive Rating',
        xaxis=dict(
            title='Offensive Pace'
        ),
        yaxis=dict(
            title='Offensive Rating'
        )
    )
    traces[1] = go.Scatter(
        x=plot_df['TOTAL_POSSESSIONS'] / plot_df['DEF_TOP'],
        y=plot_df['DRTG'],
        text=plot_df['TEAM_NAME']
    )
    layouts[1] = go.Layout(
        title='Defensive Pace vs Defensive Rating',
        xaxis=dict(
            title='Defensive Pace'
        ),
        yaxis=dict(
            title='Defensive Rating'
        )
    )
    figs = [go.Figure(data=[traces[0]], layout=layouts[0]), go.Figure(data=[traces[1]], layout=layouts[1])]
    py.iplot(figs[0], filename='pace/offensive')
    py.iplot(figs[1], filename='pace/defensive')

get_data()
