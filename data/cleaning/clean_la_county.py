import psycopg2.extras
import os
import sys

current_dir = os.path.dirname(__file__)
config_dir = os.path.join(current_dir, '..', 'db_config')
sys.path.append(config_dir)
import config as cf

def clean_parcelData():
    #modeled after https://www.postgresqltutorial.com/postgresql-python/delete/
    conn = None
    #we can keep track of how many rows we're deleting
    # to see if our cleaning method is helpful
    try:

        params = cf.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        #deleting rows based on anna's work
        cur.execute(
            "DELETE FROM rawParcelData WHERE GeneralUseType = 'Residential' ")
        cur.execute("DELETE FROM rawParcelData WHERE GeneralUseType is null")
        cur.execute("DELETE FROM rawParcelData WHERE isTaxableParcel? = 'N' ")
        cur.execute("DELETE FROM rawParcelData WHERE ZIPcode5 is null")
        cur.execute("DELETE FROM rawParcelData WHERE RollYear is null")
        cur.execute("DELETE FROM rawParcelData WHERE LandBaseYear is null")
        cur.execute("DELETE FROM rawParcelData WHERE LandValue is null")
        cur.execute("DELETE FROM rawParcelData WHERE SQFTmain = '0' ")
        cur.execute("DELETE FROM rawParcelData WHERE rowID is null")
        cur.execute(
            "DELETE FROM rawParcelData WHERE Location 1 = '(0.0°, 0.0°)'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LON = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT is null")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT is null")
        cur.execute(
            "UPDATE rawParcelData SET sqftmain = REPLACE(sqftmain, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_landvalue = REPLACE(roll_landvalue, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_impvalue = REPLACE(roll_impvalue, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_totlandimp = REPLACE(roll_totlandimp, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_realestateexemp = REPLACE(roll_realestateexemp, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_fixturevalue = REPLACE(roll_fixturevalue, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_fixtureexemp = REPLACE(roll_fixtureexemp, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_perspropvalue = REPLACE(roll_perspropvalue, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_perspropexemp = REPLACE(roll_perspropexemp, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_totalvalue = REPLACE(roll_totalvalue, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET roll_totalexemption = REPLACE(roll_totalexemption, ‘,’, ‘’)")
        cur.execute(
            "UPDATE rawParcelData SET nettaxablevalue = REPLACE(nettaxablevalue, ‘,’, ‘’)")

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
