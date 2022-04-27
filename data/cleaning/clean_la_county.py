import psycopg2.extras
import os
import sys

current_dir = os.path.dirname(__file__)
config_dir = os.path.join(current_dir, '..', 'db_config')
sys.path.append(config_dir)
import config as cf


def clean_raw_la_data():
    #modeled after https://www.postgresqltutorial.com/postgresql-python/delete/
    conn = None
    #we can keep track of how many rows we're deleting
    # to see if our cleaning method is helpful
    # try:

    params = cf.config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # make copy of raw table
    cur.execute("DROP TABLE IF EXISTS cleanlacountytable")
    cur.execute(
        "CREATE TABLE cleanlacountytable AS SELECT * FROM rawlacountytable")

    # clean table
    delete_conditions = ['GeneralUseType is null', "GeneralUseType = 'Residential'", "isTaxableParcel = 'N'",
                         'ZIPcode5 is null', "RollYear is null", 'LandBaseYear is null', 'LandValue is null',
                         "LandValue = '0'", "SQFTmain = '0'", 'rowID is null', "CENTER_LON = '0'", "CENTER_LAT = '0'",
                         'CENTER_LAT is null', 'CENTER_LON is null']
    delete_conditions = " OR ".join(delete_conditions)
    delete_stmt = "DELETE FROM cleanlacountytable WHERE " + delete_conditions
    cur.execute(delete_stmt)

    #save changes to the database
    conn.commit()
    deletedRows = cur.rowcount

    #close cursor + connection
    cur.close()
    print(f"deleted {deletedRows} rows")
    conn.close()

    return


if __name__ == "__main__":
    clean_raw_la_data()
