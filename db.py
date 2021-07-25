import sqlite3
from sqlite3 import Error
from datetime import date

class DB:

    def update_date_format(self):
        sql = "SELECT * from water"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            dt = row[0]
            if "/" in dt:
                dt = list(map(int, dt.split('/')))
                dt = date(dt[2],dt[0], dt[1])
                sql = f"UPDATE water SET date='{str(dt)}' where date='{row[0]}' and reservoir='{row[1]}'"
                cur.execute(sql)
        self.conn.commit()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # Note in cretion we can postpone commit to after all
    # data is inserted, else it takes longer
    # hence there is a separate commit method
    # if you want to commit immediately pass True here.
    def create_water_record(self, data, commit = False):
        """
        Create a new data into the water table
        :param data: (date, reservoir, level_ft, storage_tmc, inflow_cusecs, outflow_cusecs, forecast)
        :return: data id
        """
        sql = '''INSERT INTO water(date, reservoir, level_ft, storage_tmc, inflow_cusecs, outflow_cusecs, forecast)
                VALUES(?,?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, data)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def display_all_water_data(self, reservoir):
        sql = f"SELECT * FROM water WHERE reservoir='{reservoir}'"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def get_water_record(self, day, reservoir):
        sql = f"SELECT * FROM water WHERE date='{day}' and reservoir='{reservoir}'"
        #print(sql)
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows[0]

    def upsert_water_record(self, data, commit=False):
        """
        Create a new data into the water table
        :param data: (date, reservoir, level_ft, storage_tmc, inflow_cusecs, outflow_cusecs, forecast)
        :return: data id
        """
        cur = self.conn.cursor()
        sql = f"SELECT * FROM water WHERE date='{data[0]}' and reservoir='{data[1]}'"
        
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:
            # update
            sql = '''UPDATE water SET date=?, reservoir=?, level_ft=?, storage_tmc=?, 
                     inflow_cusecs=?, outflow_cusecs=?, forecast=?
                     WHERE date='{data[0]}' and reservoir='{data[1]}' '''
            cur.execute(sql, data)
            if commit:
                self.conn.commit()
            print("UPDATING...", data[0], data[1])
            return cur.lastrowid
        else:
            # insert
            print("INSERTING...", data[0], data[1])
            return self.create_water_record(data, commit)

    def create_weather_record(self, data, commit=False):
        """
        Create a new data into the weather table
        :param data: (date, location, max_temp, min_temp, temp, precip, wind, wind_dir, visibility, cloudcover, humidity, forecast)
        :return: data id
        """
        sql = '''INSERT INTO weather(date, location, max_temp, min_temp, temp, precip, wind, wind_dir, visibility, cloudcover, humidity, forecast)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, data)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def upsert_weather_record(self, data, commit=False):
        """
        Create a new data into the weather table
        :param data: (date, location, max_temp, min_temp, temp, precip, wind, wind_dir, visibility, cloudcover, humidity, forecast)
        :return: data id
        """
        cur = self.conn.cursor()
        sql = f"SELECT * FROM weather WHERE date='{data[0]}' and location='{data[1]}'"
        
        cur.execute(sql)
        rows = cur.fetchall()
        if len(rows) > 0:
            # update
            sql = '''UPDATE weather SET date=?, location=?, max_temp=?, min_temp=?, temp=?, precip=?, wind=?, 
                     wind_dir=?, visibility=?, cloudcover=?, humidity=?, forecast=?
                     WHERE date='{data[0]}' and location='{data[1]}' '''
            cur.execute(sql, data)
            if commit:
                self.conn.commit()
            print("UPDATING...", data[0], data[1])
            return cur.lastrowid
        else:
            # insert
            print("INSERTING...", data[0], data[1])
            return self.create_weather_record(data, commit)
        

    def display_all_weather(self):
        """
        Query all rows in the weather table
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM weather")

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def commit(self):
        self.conn.commit()
            
    def delete_all_weather(self):
        """
        Delete all rows in the weather table
        :return:
        """
        sql = 'DELETE FROM weather'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    def __init__(self, db_file):
        sql_create_weather_table = """ CREATE TABLE IF NOT EXISTS weather (
                                        date text NOT NULL,
                                        location text NOT NULL,
                                        max_temp real,
                                        min_temp real,
                                        temp real,
                                        precip real,
                                        wind real,
                                        wind_dir real,
                                        visibility real,
                                        cloudcover real,
                                        humidity real,
                                        forecast integer
                                    ); """

        sql_create_water_table = """ CREATE TABLE IF NOT EXISTS water (
                                        date text NOT NULL,
                                        reservoir text NOT NULL,
                                        level_ft real,
                                        storage_tmc real,
                                        inflow_cusecs real,
                                        outflow_cusecs real,
                                        forecast integer
                                    ); """


        # create a database connection
        self.conn = self.create_connection(database)

        # create tables
        if self.conn is not None:
            # create weather table
            self.create_table(sql_create_weather_table)

            # create water table
            self.create_table(sql_create_water_table)
            self.initialized = True
        else:
            print("Error! cannot create the database connection.")

 
try:
    print(appdb.initialized)
except:
    database = r"./data/pythonsqlite.db"
    appdb = DB(database)