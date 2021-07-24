import db
from datetime import date
import os
import pandas as pd

# run this initally to popylate the data. Whenever you add new files 
# remove old data and add new and run this one to insert the records.

rpath = "./data/reservoir"

for d in filter(os.DirEntry.is_file, os.scandir(rpath)):
    if d.name.endswith(".csv"):
        df = pd.read_csv(d.path)
        df["location"] = d.name[:-4].lower().strip()
        for index,row in df.iterrows():
            #(date, reservoir, level_ft, storage_tmc, inflow_cusecs, outflow_cusecs, forecast)
            data = (row['FLOW_DATE'], row['location'], row['RES_LEVEL_FT'], row['PRESENT_STORAGE_TMC'], row['INFLOW_CUSECS'], row['OUTFLOW_CUECS'], 0)
            print(data)
            db.appdb.create_water_record(data)

db.appdb.commit()

# copy all weather data csv in data/weather folder
# then write script similar to above to populate weather data table in sqlite db
# the bbotstrap script is done after that.

wpath = "./data/weather"
#db.appdb.delete_all_weather()
for d in filter(os.DirEntry.is_file, os.scandir(wpath)):
    if d.name.endswith(".csv"):
        df = pd.read_csv(d.path)
        df["location"] = d.name[:-4].lower().strip()
        for index,row in df.iterrows():
            dt = row['Date time']
            try:
                if '-' in dt:
                    dt = list(map(int, dt.split('-')))
                else:
                    dt = list(map(int, dt.split('/')))
                dt = date(dt[2], dt[1], dt[0])
            except ValueError as e:
                if 'month' in str(e):
                    dt = date(dt[2], dt[0], dt[1])
                else:
                    continue
            except Exception as e:
               continue
            
            #(date, location, max_temp, min_temp, temp, precip, wind, wind_dir, visibility, cloudcover, humidity)
            data = (str(dt), row['location'], row['Maximum Temperature'], row['Minimum Temperature'], 
                    row['Temperature'], row['Precipitation'], row['Wind Speed'],row['Wind Direction'],
                    row['Visibility'],row['Cloud Cover'],row['Relative Humidity'],0)
            #print(data)
            db.appdb.create_weather_record(data)

db.appdb.commit()
