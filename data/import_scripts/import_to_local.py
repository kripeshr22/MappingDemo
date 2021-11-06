import psycopg2
from create_table import create_table_query_2, fields_2
import os
from sodapy import Socrata


def main():
    # latest version of cleaned data schema to sue
    database = "parcelDatabase"
    tablename = "svr_table_2"
    create_table_query = create_table_query_2
    fields = fields_2

    import_to_table(database, tablename, fields, create_table_query)


# ***** connect to the db *******
def connect_to_db(database, user, password):
    try:
        conn = psycopg2.connect(database=database, user=user, password=password)
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")

    # cursor
    return conn

    

def import_to_table(database, tablename, fields, create_table_query):

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

    # uncomment the following line if schema has been updated:
    # cur.execute("DROP TABLE IF EXISTS rawParcelTable")

    # rewriting entire table for now
    cur.execute("DROP TABLE IF EXISTS " + tablename)
    cur.execute(create_table_query)
    print("created table. connecting to api")

    cols_as_string = ", ".join(fields)
    data_generator = client.get('9trm-uz8i', select="distinct " + cols_as_string,
                                    usecodedescchar1="Commercial", istaxableparcel="Y", 
                                    limit=50000)

    print("successfully got data generator from api endpoint")

    num_fields = len(fields)
    format = "(%s)" if num_fields == 1 else "(%s" + ",%s" * (num_fields - 1) + ")"

    for row in data_generator:
        # insert into table
        my_data = [row.get(field, "") for field in fields]
        insert_query = "INSERT INTO " + tablename + " VALUES " + format + " ON CONFLICT DO NOTHING"

        # -- uncomment line to show error message --
        cur.execute(insert_query, tuple(my_data))

        # -- show problem row, prevent error message --
        # try:
        #     cur.execute(insert_query, tuple(my_data))
        # except:
        #     print(my_data)
        #     break

    print("further cleaning the data")
    cur.execute("UPDATE " + tablename + " SET sqftmain = REPLACE(sqftmain, ',', '')")
    cur.execute(
        "UPDATE " + tablename + " SET roll_landvalue = REPLACE(roll_landvalue, ',', '')")
    cur.execute("DELETE FROM " + tablename + " WHERE center_lon = '0'")
    cur.execute("DELETE FROM " + tablename + " WHERE center_lat = '0'")
    cur.execute("DELETE FROM " + tablename + " WHERE roll_landbaseyear = '0'")
    conn.commit()

    print("closing cursor and connection")
    # close the cursor
    cur.close()

    # close the connection
    conn.close()



