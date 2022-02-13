# This file is to test the .ini and config.py files
# Mariesa Teo
import psycopg2
from sodapy import Socrata
from config import config

def main():
    try:

        params = config()
        conn = psycopg2.connect(**params)
        
        print("I am connected to the database")

        cur = conn.cursor()

        cur.execute('SELECT count(*) from cleanlacountytable;', [])
        results = cur.fetchone()
        print(results)

        #close cursor
        cur.close()
    except:
        print("I am unable to connect to the database")
    finally:
        #close connection to heroku
        conn.close()
        print("finished")
