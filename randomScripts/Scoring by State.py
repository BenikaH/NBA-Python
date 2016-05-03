# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib
from bs4 import BeautifulSoup
import pandas as pd
import plotly.plotly as py

url = "http://www.basketball-reference.com/friv/birthplaces.cgi"
html = urllib.urlopen(url)
soup = BeautifulSoup(html)
aTags = soup.findAll('a')
links = []
names = []
for row in aTags:
    links.append(row.get('href'))
    names.append(row.getText())
links = links[33:83]
names = names[33:83]
del links[8]
del names[8]
states = [0] * 49
df = pd.DataFrame()
for i in range(len(links)):
    tempUrl = url + links[i]
    tempHtml = urllib.urlopen(tempUrl)
    tempSoup = BeautifulSoup(tempHtml)
    column_headers = [th.getText() for th in tempSoup.findAll('tr')[29].findAll('th')]
    data_rows = tempSoup.findAll('tr')[30:]
    player_data = [[td.getText() for td in data_rows[j].findAll('td')] for j in range(len(data_rows))]
    tempDf = pd.DataFrame(player_data, columns=column_headers)
    states[i] = links[i].split('=')[2]
    tempDf = tempDf.convert_objects(convert_numeric=True)
    tempDf = tempDf[:].fillna(0)
    tempDf = tempDf.ix[:, 0:19]
    tempDf['State'] = links[i].split('=')[2]
    if df.size == 0:
        df = tempDf
    else:
        df = df.append(tempDf)
        
statePoints = [0] * 49

for i in range(len(states)):
    state = links[i].split('=')[2]
    stateDf = df.loc[df['State'] == state]
    statePoints[i] = stateDf['PTS'].sum()

pop = pd.read_csv("statePop.csv")
pop = pop.ix[:,2]

data = [dict(
    type='choropleth',
    autocolorscale=True,
    locations=states,
    z=statePoints,
    locationmode='USA-states',
    text=statePoints,
    marker=dict(
        line=dict(
            color='rgb(255,255,255)',
            width=2
        )
    ),
    colorbar=dict(
        title="Points"
    )
)]

layout = dict(
    title='NBA points by player birth state',
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
    ),
)

fig = dict(data=data, layout=layout)
url = py.plot(fig, filename='byState/pointsByBirthState')

statePoints = statePoints / pop

data = [dict(
    type='choropleth',
    autocolorscale=True,
    locations=states,
    z=statePoints,
    locationmode='USA-states',
    text=statePoints,
    marker=dict(
        line=dict(
            color='rgb(255,255,255)',
            width=2
        )
    ),
    colorbar=dict(
        title="Points"
    )
)]

layout = dict(
    title='NBA points by player birth state / population',
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
    ),
)

fig = dict(data=data, layout=layout)
url = py.plot(fig, filename='byState/pointsByBirthStateOverPop')
