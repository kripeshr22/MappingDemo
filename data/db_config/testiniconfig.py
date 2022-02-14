# This file is to test the .ini and config.py files
# Currently set up to work in python files in both data and in subfolders of data eg. find_case_studies
# Mariesa Teo
import psycopg2
from sodapy import Socrata
import db_config

def main():
    try:

        params = db_config.config()
        conn = psycopg2.connect(**params)
        
        print("I am connected to the database")

        cur = conn.cursor()

    # Print the number of rows in this table to prove that we are connecting to the database
        cur.execute('SELECT count(*) from cleanlacountytable;', [])
        results = cur.fetchone()
        print(results)

        #close cursor and database connection
        cur.close()
        conn.close()
        print("finished")
    except:
        print("I am unable to connect to the database")
