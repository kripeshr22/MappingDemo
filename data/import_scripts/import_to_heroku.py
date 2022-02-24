from pkgutil import get_data
import psycopg2 as pg
import psycopg2.extras
from create_table import raw_socrata_table_schema, all_fields_socrata
from sodapy import Socrata


import os
import sys

current_dir = os.path.dirname( __file__ )
config_dir = os.path.join( current_dir, '..', 'db_config' )
sys.path.append( config_dir )
import config as cf

def main():
    # tablename = "rawlacountytable"
    # primary_key = "rowID"
    # import_from_api_to_heroku(all_fields_socrata, tablename,
    #                           primary_key, raw_socrata_table_schema)

    tablename = "testtable"
    primary_key = "rowID"
    county_name = "la"
    import_from_api_to_heroku(all_fields_socrata, tablename, county_name,
                              primary_key, raw_socrata_table_schema)

def connect_to_heroku_db():
    conn = ""
    # connect to standard-0 heroku db
    try:
        params = cf.config()
        conn = psycopg2.connect(**params)
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")
    
    return conn

def get_client(county_name):
    # get df id and endpoint root from datasources.ini
    token = cf.app_token()
    info = cf.datasource_info(section=county_name)

    client = Socrata(
        info['endpoint'],
        # tech equity token for socrata api access
        app_token=token,
        timeout=1000000
    )
    return client

def get_dataset_id(county_name):
    info = cf.datasource_info(section=county_name)
    return info['dataset_id']

# ***** connect to the db and api *******
def import_from_api_to_heroku(fields, tablename, county_name, primary_key, 
    create_table_query="", rewrite_table=False):

    # client = Socrata(
    #     "data.lacounty.gov",
    #     app_token='8uMOnLx6S823qlm58la47e6Pd', # tech equity token for socrata api access
    #     timeout=1000000
    # )

    conn = connect_to_heroku_db()
    if (conn == ""):
        return

    # cursor
    cur = conn.cursor()

    # rewriting entire table 
    if rewrite_table:
        cur.execute("DROP TABLE IF EXISTS " + tablename)
        cur.execute(create_table_query)
        conn.commit()
        print("created table. connecting to api")


    # Retrieve Json Data from API endpoint
    cols_as_string = ", ".join(fields)
    insert_query = "INSERT INTO " + tablename + " VALUES %s ON CONFLICT DO NOTHING;"
    client = get_client(county_name)
    dataset_id = get_dataset_id(county_name)

    num_records = client.get_all(dataset_id, select="count(*)")
    num_records = int(next(num_records).get("count"))
    print("Total of ", num_records, " records attempted to insert")

    ### page size = 1000 -> 33k rows/min
    ### page size = 25k -> 50k rows/50 sec
    ### page size = 50k -> 50k rows/38 sec
    offset = 0
    limit = 25000

    try:
        print("Inserting data")

        while(offset < num_records):
            data_generator = client.get(dataset_id, select=cols_as_string,
                                            usecodedescchar1="Commercial", istaxableparcel="Y",
                                            order=primary_key+" DESC", limit=limit, offset=offset)

            psycopg2.extras.execute_values(
                cur,
                insert_query,
                [tuple([data.get(f, "") for f in fields])
                for data in data_generator]
            )

            conn.commit()
            offset = offset + limit
            print("offset is ", offset)

    except (Exception, pg.Error) as e:
            print(e)
    finally:
        if (conn):
            cur.close()
            conn.close()
            print("Inserted data into table. Connection closed.")


