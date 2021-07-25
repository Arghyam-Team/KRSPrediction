import json
from datetime import date, timedelta
import db
from urllib.request import urlopen

# weather
def update_weather():
    today = date.today()
    end = today + timedelta(90)
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Karnataka/{str(today)}/{str(end)}?unitGroup=metric&key=7FZ7P4JVS4E9XSVBUXYRHQHRH&include=fcst%2Cstats%2Ccurrent"
    print(url)
    response = urlopen(url)
    data = json.loads(response.read())
    # with open("data/karnataka.json") as f:
    #data = json.load(f)
    for day in data["days"]:
        dt = day['datetime']
        dt = list(map(int, dt.split('-')))
        dt = date(dt[0], dt[1], dt[2])
        data = (str(dt), 'karnataka', day['tempmax'], day['tempmin'], 
                    day['temp'], day['precip'], day['windspeed'],day['winddir'],
                    day['visibility'],day['cloudcover'],day['humidity'],0 if dt<=today else 1)
        db.appdb.upsert_weather_record(data)

    db.appdb.commit()

def update_reservoir():
    pass
