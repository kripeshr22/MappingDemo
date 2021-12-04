import psycopg2 as pg
import psycopg2.extras
from create_table import create_table_query_2, fields_2
import os
from sodapy import Socrata


def main():
    # latest version of cleaned data schema to sue
    database = "parcelDatabase"
    tablename = "svr_table_2"
    create_table_query = create_table_query_2
    fields = fields_2
    primary_key = "ain"

    import_to_table(fields, database, tablename, primary_key, create_table_query)


# ***** connect to the db *******
def connect_to_db(database, user, password):
    try:
        conn = pg.connect(database=database, user=user, password=password)
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")

    # cursor
    return conn

    
def import_to_table(fields, database, tablename, primary_key, create_table_query="", rewrite_table=False):

    # for setting env variables (USER & PASSWORD): https://askubuntu.com/questions/58814/how-do-i-add-environment-variables
    conn = connect_to_db(database, os.getenv(
        "USER"), os.getenv("PASSWORD"))
    cur = conn.cursor()


    # tech equity app token for socrata api access
    client = Socrata(
        "data.lacounty.gov",
        app_token='8uMOnLx6S823qlm58la47e6Pd',
        timeout=1000
    )

    # rewriting entire table
    if rewrite_table:
        cur.execute("DROP TABLE IF EXISTS " + tablename)
        cur.execute(create_table_query)
        conn.commit()
        print("created table. connecting to api")

    cols_as_string = ", ".join(fields)

    insert_query = "INSERT INTO " + tablename + " VALUES %s ON CONFLICT DO NOTHING;"

    num_records = client.get_all('9trm-uz8i', select="count(*)")
    num_records = int(next(num_records).get("count"))
    print("Total of ", num_records, " to import")

    offset = 0
    limit = 25000

    try:
        print("Inserting data")

        while(offset < num_records):
            data_generator = client.get('9trm-uz8i', select="distinct " + cols_as_string,
                                            usecodedescchar1="Commercial", istaxableparcel="Y",
                                            order=primary_key + " DESC", limit=limit, offset=offset)

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

    # print("further cleaning the data")
    # cur.execute("UPDATE " + tablename + " SET sqftmain = REPLACE(sqftmain, ',', '')")
    # cur.execute(
    #     "UPDATE " + tablename + " SET roll_landvalue = REPLACE(roll_landvalue, ',', '')")
    # cur.execute("DELETE FROM " + tablename + " WHERE center_lon = '0'")
    # cur.execute("DELETE FROM " + tablename + " WHERE center_lat = '0'")
    # cur.execute("DELETE FROM " + tablename + " WHERE roll_landbaseyear = '0'")
    # conn.commit()

    # print("closing cursor and connection")
    # # close the cursor
    # cur.close()

    # # close the connection
    # conn.close()



