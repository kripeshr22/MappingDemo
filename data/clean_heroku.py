import psycopg2
from create_table import create_table_query
from sodapy import Socrata
from utils import profile 
from config import config

def clean_parcelData():
    #modeled after https://www.postgresqltutorial.com/postgresql-python/delete/
    conn = None
    #we can keep track of how many rows we're deleting 
    # to see if our cleaning method is helpful
    try:

        params = config()
        conn = psycopg2.connect(**params)
        
        print("I am connected to the database")

        cur = conn.cursor()
        #deleting rows based on anna's work 
        cur.execute("DELETE FROM rawParcelData WHERE usecodedescchar1 = 'Residential' ")
        cur.execute("DELETE FROM rawParcelData WHERE usecodedescchar1 is null")
        cur.execute("DELETE FROM rawParcelData WHERE istaxableparcel? = 'N' ")
        cur.execute("DELETE FROM rawParcelData WHERE situszip5 is null")
        cur.execute("DELETE FROM rawParcelData WHERE rollyear is null")
        cur.execute("DELETE FROM rawParcelData WHERE roll_landbaseyear is null")
        cur.execute("DELETE FROM rawParcelData WHERE roll_landvalue is null")
        cur.execute("DELETE FROM rawParcelData WHERE sqftmain = '0' ")
        cur.execute("DELETE FROM rawParcelData WHERE rowid is null")
        cur.execute("DELETE FROM rawParcelData WHERE center_lon = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE center_lat = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE center_lat is null")
        cur.execute("UPDATE rawParcelData SET sqftmain = REPLACE(sqftmain, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_landvalue = REPLACE(roll_landvalue, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_impvalue = REPLACE(roll_impvalue, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_totlandimp = REPLACE(roll_totlandimp, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_realestateexemp = REPLACE(roll_realestateexemp, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_fixturevalue = REPLACE(roll_fixturevalue, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_fixtureexemp = REPLACE(roll_fixtureexemp, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_perspropvalue = REPLACE(roll_perspropvalue, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_perspropexemp = REPLACE(roll_perspropexemp, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_totalvalue = REPLACE(roll_totalvalue, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET roll_totalexemption = REPLACE(roll_totalexemption, ‘,’, ‘’)")
        cur.execute("UPDATE rawParcelData SET nettaxablevalue = REPLACE(nettaxablevalue, ‘,’, ‘’)")


        #updating our number of deleted rows based on what we removed
        deletedRows = cur.rowcount
        #save changes to the database
        conn.commit()
        #close cursor
        cur.close()
    except:
        print("I am unable to connect to the database")
    finally:
        #close connection to heroku
        conn.close()
    return deletedRows