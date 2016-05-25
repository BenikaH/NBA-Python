from stravalib.client import Client
from stravalib import unithelper

client = Client(access_token="c4f46d9b575b4ed3b3bd5605a8627a2e87326710")
athlete = client.get_athlete()
activities = client.get_activities()
for activity in activities:
    if activity.type == 'Run':
        distance = (unithelper.miles(activity.distance))
        time = activity.moving_time.seconds
        speed = float(time) / (float(distance) * 60)
        date = activity.start_date
        print("On " + str(date) + ", you ran " + str(distance) + " miles in " + str(
            time) + " seconds. Giving you a pace of " + str(speed) + " minutes per mile")
