import json
from datetime import date, timedelta
import db
from urllib.request import urlopen
from bs4 import BeautifulSoup
from setup import MODELS
from forecasting import predict, predict_from_weather
import os
# weather
def update_weather(today = date.today()):
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
        
            
def run_predictions(dt=date.today()):
    "predictions will be in forecast table"
    "we can always compare them with actual data as future evolves"
    afterdate = dt
    for m in MODELS:
        print("Now running model", m["number"], "-", m["title"])
        if m.get('onlyweather', False):
            predict_from_weather(m, afterdate)
        else:
            predict(m, afterdate)

# TODO cron job to run daily


# TODO cron jub to run weekly or monthly or manually done
# re-train all the models on new data



def old_predictions():
    for m in MODELS:
        afterdate = date(2019,12,31)
        while afterdate<date.today():
            if m.get('onlyweather', False):
                predict_from_weather(m, afterdate)
                afterdate += timedelta(30)
            else:
                predict(m, afterdate)
                afterdate += timedelta(m['HORIZON'])

dir_path = os.path.dirname(os.path.realpath(__file__))

def modelInfo():
    global dir_path
    from tensorflow import keras    
    for m in MODELS:
        checkpoint_filepath = os.path.join(dir_path, f"models/{m['folder']}")
        model = keras.models.load_model(checkpoint_filepath)
        print(m['title'])
        model.summary()

#old_predictions()

#modelInfo()

#update_weather()
#update_reservoir()
# end = date(2021,1,1)
# dt = date.today() - timedelta(17)
# while dt < date.today():
#      update_reservoir(dt)
#      dt += timedelta(1)
#db.appdb.update_date_format()
#db.appdb.display_all_water_data("kabini")


#for i in range(17, -1, -1):
#    run_predictions(date.today() - timedelta(i))
#    update_reservoir(date.today() - timedelta(i))

dt = date.today()
update_weather(dt)
update_reservoir(dt)
run_predictions(dt)

with open(os.path.join(dir_path, "lastupdatedon.txt"), "w") as out:
     out.write(str(date.today()))


os.chdir('/home/abhinav/KRSPrediction')
os.system(f'git commit -a -m "updated {str(date.today())}"')
os.system('git push')
