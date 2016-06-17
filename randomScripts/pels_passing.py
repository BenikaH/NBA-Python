from dataGetters import j2p
import pandas as pd
import plotly.plotly as py
from plotly.tools import FigureFactory as FF


def build_freq_csv():
    url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID=1610612740&VsConference=&VsDivision="
    df = j2p(url, 1)
    df = df.sort_values(by='MIN', ascending=False).head(10)
    playerNames = df['PLAYER_NAME'].tolist()
    playerIds = df['PLAYER_ID'].tolist()
    passDf = pd.DataFrame(columns=playerNames)
    passDf['PASS_FROM'] = playerNames

    playerUrlTemplate = "http://stats.nba.com/stats/playerdashptpass?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=PerGame&Period=0&PlayerID={id}&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="

    for iter, id in enumerate(playerIds):
        playerName = playerNames[iter]
        playerUrl = playerUrlTemplate.format(id=id)
        playerDf = j2p(playerUrl, 0)
        passDfIndex = passDf[passDf['PASS_FROM'] == playerName].index
        for index2, teammate in playerDf.iterrows():
            teammateName = str(teammate.PASS_TO)
            teammateName = teammateName.split(', ')
            teammateName = teammateName[1] + ' ' + teammateName[0]
            if teammateName in passDf.columns.values:
                passDf.ix[passDfIndex, teammateName] = teammate.FREQUENCY

    passDf.fillna(0)
    passDf.to_csv('pelicans_passing.csv')


def build_totals_csv():
    url = "http://stats.nba.com/stats/teamplayerdashboard?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID=1610612740&VsConference=&VsDivision="
    df = j2p(url, 1)
    df = df.sort_values(by='MIN', ascending=False).head(10)
    playerNames = df['PLAYER_NAME'].tolist()
    playerIds = df['PLAYER_ID'].tolist()
    passDf = pd.DataFrame(columns=playerNames)
    passDf['PASS_FROM'] = playerNames

    playerUrlTemplate = "http://stats.nba.com/stats/playerdashptpass?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=Totals&Period=0&PlayerID={id}&Season=2015-16&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="

    for iter, id in enumerate(playerIds):
        playerName = playerNames[iter]
        playerUrl = playerUrlTemplate.format(id=id)
        playerDf = j2p(playerUrl, 0)
        passDfIndex = passDf[passDf['PASS_FROM'] == playerName].index
        for index2, teammate in playerDf.iterrows():
            teammateName = str(teammate.PASS_TO)
            teammateName = teammateName.split(', ')
            teammateName = teammateName[1] + ' ' + teammateName[0]
            if teammateName in passDf.columns.values:
                passDf.ix[passDfIndex, teammateName] = teammate.PASS

    passDf.fillna(0)
    passDf.to_csv('pelicans_passing_totals.csv')


def build_heat_map(csv_name, plot_name, decimals):
    df = pd.read_csv(csv_name)
    df1 = df.drop('PASS_FROM', 1)
    df1 = df1.fillna(0)
    if decimals > 0:
        df1 = df1.round(decimals=decimals)
    else:
        df1 = df1.astype(int)
    z = df1.as_matrix(columns=df1.columns.values[1:]) * 100
    print("Columns: " + str(len(z)))
    print("Rows: " + str(len(z[0])))
    print(z)
    x = df1.columns.values[1:].tolist()
    print(len(x))
    fig = FF.create_annotated_heatmap(z, x=x, y=x, colorscale='Viridis')
    py.iplot(fig, filename=plot_name)


# build_freq_csv()
# build_totals_csv()
# build_heat_map('pelicans_passing.csv', 'pelicans_passing/frequency', 2)
build_heat_map('pelicans_passing_totals.csv', 'pelicans_passing/totals', 0)