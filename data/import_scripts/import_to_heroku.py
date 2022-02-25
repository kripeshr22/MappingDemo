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


### page size = 1000 -> 33k rows/min
### page size = 25k -> 50k rows/50 sec
### page size = 50k -> 50k rows/38 sec
## TODO: is this the best way to specify limit? maybe put in config file (with offset) 
# + pull variable
LIMIT = 25000 

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


def get_data_generator(county_name, fields, primary_key, client, offset):
    dataset_id = get_dataset_id(county_name)
    cols_as_string = ", ".join(fields)

    data_generator = client.get(dataset_id, select=cols_as_string,
                                usecodedescchar1="Commercial", istaxableparcel="Y",
                                order=primary_key+" DESC", limit=LIMIT, offset=offset)

    return data_generator

# ***** connect to the db and api *******
def import_from_api_to_heroku(county_name, tablename, primary_key, fields,
    create_table_query="", rewrite_table=False):

    conn = connect_to_heroku_db()
    if (conn == ""):
        return

    cur = conn.cursor()

    # rewriting entire table if flagged
    if rewrite_table:
        cur.execute("DROP TABLE IF EXISTS " + tablename)
        cur.execute(create_table_query)
        conn.commit()
        print("created table. connecting to api")


    # Retrieve Json Data from API endpoint
    insert_query = "INSERT INTO " + tablename + " VALUES %s ON CONFLICT DO NOTHING;"
    client = get_client(county_name)
    dataset_id = get_dataset_id(county_name)

    ## TODO: put this in a log file instead of printing
    num_records = client.get_all(dataset_id, select="count(*)")
    num_records = int(next(num_records).get("count"))
    print("Total of ", num_records, " records attempted to insert")

    offset = 0
    try:
        print("Inserting data")
        while(offset < num_records):
            data_generator = get_data_generator(county_name, fields, primary_key, client, offset)
            psycopg2.extras.execute_values(
                cur,
                insert_query,
                [tuple([data.get(f, "") for f in fields])
                for data in data_generator]
            )

            conn.commit()
            offset = offset + LIMIT
            ## TODO: print this into a log file instead of to terminal
            print("offset is ", offset)

    except (Exception, pg.Error) as e:
            print(e)
    finally:
        if (conn):
            cur.close()
            conn.close()
            print("Inserted data into table. Connection closed.")


def main():
    tablename = "rawlacountytable"
    primary_key = "rowID"
    import_from_api_to_heroku(all_fields_socrata, tablename,
                              primary_key, raw_socrata_table_schema)

    ## TODO: take these parameters in as args using argparser
    ## link schemas with tablename -> search for appropriate fields + schema
    ## in schema dictionary
    # tablename = "testtable"
    # primary_key = "rowID"
    # county_name = "sf"
    # import_from_api_to_heroku(
    #     county_name, tablename, primary_key, all_fields_socrata, raw_socrata_table_schema, True)

## take in args here
if __name__ == "__main__":
    main()
