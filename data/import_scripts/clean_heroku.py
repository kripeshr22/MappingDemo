import psycopg2


def main():
    # latest version of cleaned data schema to sue

    # ADD CORRECT INFO HERE
    database = ""
    tablename = "cleanlacountytable"
    user=""
    password=""
    port=""
    host=""


    clean_table(database, tablename, user, password, port, host)
    #connect_to_db(database, user, password, port, host)


# ***** connect to the db *******
def connect_to_db(database, user, password, port, host):
    conn = ""
    # conn = psycopg2.connect(database=database, user=user, password=password)
    # print("conn is ", conn)
    try:
        conn = psycopg2.connect(database=database, user=user, password=password, sslmode='require', port=port, host=host)
        print("successfully connected to database")
    except Exception as e: 
        print("I am unable to connect to the database")
        print(e)

    # cursor
    return conn

    

def clean_table(database, tablename, user, password, port, host):

    conn = connect_to_db(database, user, password, port, host)
    cur = conn.cursor()

    print("further cleaning the data")
    cur.execute("UPDATE " + tablename + " SET sqftmain = REPLACE(sqftmain, ',', '')")
    cur.execute(
        "UPDATE " + tablename + " SET landvalue = REPLACE(landvalue, ',', '')")
    cur.execute("DELETE FROM " + tablename + " WHERE center_lon = '0'")
    cur.execute("DELETE FROM " + tablename + " WHERE center_lat = '0'")
    cur.execute("DELETE FROM " + tablename + " WHERE landbaseyear = '0'")
    cur.execute("DELETE FROM " + tablename + " WHERE sqftmain = '0'")
    #DELETE FROM svr_table_2 where (situszip5 !~ '^[0-9]+$'); - deletes NaN values from situszip
    cur.execute("DELETE FROM " + tablename + " WHERE (zipcode5 !~ '^[0-9]+$')")
    #DELETE FROM svr_table_2 where (center_lon !~ '^-?[0-9][0-9,\.]+$');   - deletes NaN values from center_lon
    cur.execute("DELETE FROM " + tablename + " WHERE (center_lon !~ '^-?[0-9][0-9,\.]+$')")
    # delete if effective year built is 0
    cur.execute("DELETE FROM " + tablename + " WHERE (effectiveyearbuilt = '0')")
    # some effective year built values where double digit numbers - this gets rid of them
    cur.execute("DELETE FROM " + tablename + " WHERE (LENGTH(effectiveyearbuilt) < 4)")
    # some year built values where double digit numbers - this gets rid of them
    cur.execute("DELETE FROM " + tablename + " WHERE (LENGTH(yearbuilt) < 4)")
    # delete when landvalue is 0
    cur.execute("DELETE FROM " + tablename + " WHERE landvalue = '0'")
    # delete rows where land value is less than 1000
    cur.execute("DELETE FROM " + tablename + " WHERE (CAST(landvalue AS DOUBLE PRECISION)<10000)")
    # delete rows where sqft is less than 75 (smallest homes are usually abpve 80sqft)
    cur.execute("DELETE FROM " + tablename + " WHERE (CAST(sqftmain AS DOUBLE PRECISION)<75)")
    print("done cleaning")
    conn.commit()

    print("closing cursor and connection")
    # close the cursor
    cur.close()

    # close the connection
    conn.close()
