from import_to_heroku import connect_to_heroku_db 
from create_table import create_raw_table, csv_fields
import csv
import psycopg2 as pg


# running script from clinic computer to import csv into heroku
def main():
    fields = csv_fields
    create_table_query = create_raw_table
    tablename = "rawLACountyTable"
    filepath = '/Users/clinic21/Desktop/commercial_parcel_data.csv'

    import_csv_to_heroku(tablename, create_table_query, fields, filepath)

def get_insert_query(tablename, fields):
    num_fields = len(fields)
    format = "(%s)" if num_fields == 1 else "(%s" + ",%s" * (num_fields - 1) + ")"

    sql_insert = "INSERT INTO " + tablename + " VALUES" + format

    return sql_insert

def import_csv_to_heroku(tablename, create_table_query, fields, filepath):
    ## connect to heroku ##
    conn = connect_to_heroku_db()
    if (conn == ""):
        return

    # cursor
    cur = conn.cursor()

    # create table 
    cur.execute("DROP TABLE IF EXISTS " + tablename)
    cur.execute(create_table_query)
    print("Created " + tablename + ". Inserting CSV into table")

    # insert csv into table
    sql_insert = get_insert_query(tablename, fields)
    try:
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) # This skips the 1st row which is the header.
            for record in reader:
                cur.execute(sql_insert, record)
                conn.commit()
    except (Exception, pg.Error) as e:
            print(e)
    finally:
        if (conn):
            cur.close()
            conn.close()
            print("Inserted CSV into table. Connection closed.")



