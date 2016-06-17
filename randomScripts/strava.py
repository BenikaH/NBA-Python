from stravalib.client import Client
from stravalib import unithelper
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

client = Client(access_token="7a3d420066da21add6fdfb7713ebc0168bf01617")
athlete = client.get_athlete()
activities = client.get_activities()

activitiesDf = pd.DataFrame(columns=['Date', 'Distance', 'Time', 'Pace'])

for activity in activities:
    if activity.type == 'Run':
        distance = (unithelper.miles(activity.distance)).get_num()
        time = activity.moving_time.seconds
        pace = time / (distance * 60)
        date = activity.start_date
        newRow = [date, distance, time, pace]
        activitiesDf = activitiesDf.append(pd.Series(newRow, index=['Date', 'Distance', 'Time', 'Pace']),
                                           ignore_index=True)

trace = go.Scatter(
    x=activitiesDf['Date'],
    y=activitiesDf['Distance'],
    text=activitiesDf['Pace'],
    mode='markers',
    marker=dict(
        color=activitiesDf['Pace'].max() - activitiesDf['Pace'],
        colorscale='RdYlBu',
        showscale=True,
        size=10
    )
)

data = [trace]
py.iplot(data, filename='Hiking_Strava')
