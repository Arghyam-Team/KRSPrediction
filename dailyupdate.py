import json
from datetime import date, timedelta
import db
from urllib.request import urlopen
from bs4 import BeautifulSoup
from config.setup import MODELS
from forecasting import forecasting
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

def update_reservoir(today = date.today()):
    def reservoir_name(givenname):
        if givenname.lower().startswith("krishna"):
            return "krs"
        elif givenname.lower().startswith("kabini"):
            return "kabini"
        elif givenname.lower().startswith("harangi"):
            return "harangi"
        else:
            return "hemavathi"

    baddata = {
        "krs": [103.38, 25577.0, 20796.0, 4233.0],
        "kabini": [62.1, 17697.0, 23129.0, 20675.0],
        "harangi": [124.48, 6970.0, 9783.0, 14003.0],
        "hemavathi": [105.68, 27198.0, 20871.0, 410.0]
    }

    url = f"http://122.15.179.102/ARS/home/reservoir/{str(today)}"
    print(url)
    response = urlopen(url)
    bs = BeautifulSoup(response.read(),features="html.parser")
    prevday = today + timedelta(-1)
    print(prevday)
    table = bs.find('table')
    rows = table.findAll('tr', {'class':'bg-primary'})
    for row in rows:
        level = float(row.findAll('td')[3].string)
        storage = float(row.findAll('td')[4].string)
        inflow = float(row.findAll('td')[5].string)
        outflow = float(row.findAll('td')[6].string)
        reservoir = reservoir_name(row.find('td').string.split('-')[0].strip())
        isbad =  [level, storage, inflow, outflow] == baddata[reservoir]
        data = (str(today), reservoir, level, storage/1000, inflow, outflow)
        if isbad:
            print("Improper data found, reverting to previous day data...")
            old = db.appdb.get_water_record(str(prevday), reservoir)
            data = (str(today), *old[1:-1])
        print(data)
        db.appdb.upsert_water_record(data, True)
        
            
def run_predictions():
    "predictions will be in forecast table"
    "we can always compare them with actual data as future evolves"
    afterdate = date.today()
    for model in MODELS:
        print("Now running model", model["number"], "-", model["title"])
        forecasting.predict(model, afterdate)

# TODO cron job to run daily
update_weather()
update_reservoir()
run_predictions()

# TODO cron jub to run weekly or monthly or manually done
# re-train all the models on new data

# end = date(2021,1,1)
# dt = date(2020,12,17)
# while dt < end:
#     update_reservoir(dt)
#     dt += timedelta(1)
#db.appdb.update_date_format()
#db.appdb.display_all_water_data("kabini")