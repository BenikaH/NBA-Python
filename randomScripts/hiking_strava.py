from stravalib.client import Client
from stravalib import unithelper
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

client = Client(access_token="7a3d420066da21add6fdfb7713ebc0168bf01617")
athlete = client.get_athlete()
activities = client.get_activities()
hike = 0

for activity in activities:
    if activity.name == "HIKE":
        hike = activity

print(hike.map)
print(hike.map.polyline)