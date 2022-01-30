import psycopg2
from create_table import create_table_query
from utils import profile 


def clean_KNN():
    try:
        #use your username and password for your local database since we do not want to alter
        #heroku with model specific cleaning!
        conn = psycopg2.connect(database='parcelDatabase', user='user', password='password')
        print("successfully connected to database")
        # cursor
        cur = conn.cursor() 
        #insert other cleaning
        cur.execute("SELECT sqftmain, roll_landvalue, roll_landbaseyear, center_lat, center_lon from rawparceltable")
        cur.execute("DELETE FROM rawParcelData WHERE sqftmain = '0' ")
        cur.execute("ALTER TABLE rawparceldata")
        cur.execute("ALTER COLUMN roll_landbaseyear TYPE INT")
        cur.execute("ALTER COLUMN sqftmain TYPE FLOAT")
        cur.execute("ALTER COLUMN roll_landvalue TYPE FLOAT")
        cur.execute("ALTER COLUMN center_lat TYPE FLOAT")
        cur.execute("ALTER COLUMN center_lon TYPE FLOAT")

        #save changes to the database
        conn.commit()
        #close cursor
        cur.close()
    except:
        print("I am unable to connect to the database")
    finally:
        #close connection to heroku
        conn.close()