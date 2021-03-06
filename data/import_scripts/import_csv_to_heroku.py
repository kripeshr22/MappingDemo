from import_to_heroku import connect_to_heroku_db, get_insert_query, prevent_repeat_inserts_prefix
from create_table import create_raw_table, csv_fields
import csv
import psycopg2 as pg

import os
import sys
current_dir = os.path.dirname( __file__ )
config_dir = os.path.join( current_dir, '..', 'db_config' )
sys.path.append( config_dir )
import config as cf


# running script from clinic computer to import csv into heroku
def main():
    fields = csv_fields
    create_table_query = create_raw_table
    tablename = "rawLACountyTable"
    filepath = '/Users/clinic21/Desktop/commercial_parcel_data.csv'

    import_csv_to_heroku(tablename, create_table_query, fields, filepath)



def import_csv_to_heroku(tablename, create_table_query, fields, filepath):
    ## connect to heroku ##
    conn = connect_to_heroku_db()
    if (conn == ""):
        return

    # cursor
    cur = conn.cursor()

    # create table 
    # cur.execute("DROP TABLE IF EXISTS " + tablename)
    # cur.execute(create_table_query)
    # print("Created " + tablename + ". Inserting CSV into table")

    # insert csv into table
    sql_insert = get_insert_query(tablename, fields)

    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) # This skips the 1st row which is the header.
            for record in reader:
                row_id = record[-4]
                query_prefix = prevent_repeat_inserts_prefix(tablename, row_id)
                query_wrapped = "DO\n$do$\nBEGIN\n" + "\t" + query_prefix + " THEN\n\t\t" + \
                                sql_insert + ";\n\tEND IF;\nEND\n$do$"

                cur.execute(query_wrapped, record)
                conn.commit()
    except (Exception, pg.Error) as e:
            print(e)
    finally:
        if (conn):
            cur.close()
            conn.close()
            print("Inserted CSV into table. Connection closed.")



