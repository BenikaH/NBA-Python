import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import os.path


def get_urls_for_year(year):
    url = 'http://www.basketball-reference.com/leagues/NBA_{year}.html#all_team_stats'
    url = url.format(year=year)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)

    soup = BeautifulSoup(response, "html.parser")
    table = soup.find('table', id='team')
    rows = table.findAll('a')

    urls = []

    for row in rows:
        url = 'http://www.basketball-reference.com' + row['href']
        urls.append(url)

    return urls


def get_advanced_stats_df_by_team_and_year(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)

    soup = BeautifulSoup(response, "html.parser")
    table = soup.find('table', id='advanced')
    rows = table.findAll('tr')[1:]

    column_headers = [th.getText() for th in table.findAll('th')]

    player_data = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

    return pd.DataFrame(player_data, columns=column_headers)


def get_assist_distribution(func_df):
    ast_list = []
    for row in func_df.iterrows():
        ast = row[1][12]
        minutes = row[1][4]
        for m in range(0, int(minutes)):
            ast_list.append(ast)
    nup = numpy.array(ast_list).astype(numpy.float)
    return nup.std()


def get_team_stats_by_team_and_year(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)

    soup = BeautifulSoup(response, "html.parser")
    table = soup.find('table', id='team_misc')
    rows = table.findAll('tr')[2:]
    offensive_rating = float(rows[0].findAll('td')[6].getText())

    table = soup.find('table', id='team_stats')
    rows = table.findAll('tr')[1:]
    fga = float(rows[0].findAll('td')[3].getText())
    assists = float(rows[0].findAll('td')[18].getText())

    return [offensive_rating, assists / fga]


def compile_stats(overwrite):
    if not os.path.exists('../data/assist_distribution/'):
        os.makedirs('../data/assist_distribution')

    file_path = '../data/assist_distribution/data.csv'

    if (not os.path.isfile(file_path)) or overwrite:
        df = pd.DataFrame(columns=['Year', 'Team', 'Assist_Distribution', 'Team_Assist_Percentage', 'Offensive_Rating'])
        for year in range(1990, 2017):
            urls_for_year = get_urls_for_year(year)
            for url in urls_for_year:
                year = year
                team = url.split('/')[4]
                team_df = get_advanced_stats_df_by_team_and_year(url)
                assist_std_div = get_assist_distribution(team_df)
                [offensive_rating, team_assist_percentage] = get_team_stats_by_team_and_year(url)
                row = [year, team, assist_std_div, team_assist_percentage, offensive_rating]
                print(row)
                df = df.append(pd.Series(row, index=df.columns), ignore_index=True)
        df.to_csv(file_path)


compile_stats(True)
