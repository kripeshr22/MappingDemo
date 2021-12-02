import psycopg2 as pg
import psycopg2.extras
from create_table import create_raw_table, all_fields, fields_1, create_table_query_1, test_fields, create_test_table
from sodapy import Socrata


def main():
    tablename = "testtable"
    primary_key = "rowid"
    import_from_api_to_heroku(test_fields, tablename, primary_key, create_test_table, True)

def connect_to_heroku_db():
    conn = ""
    # connect to standard-0 heroku db
    try:
        conn = pg.connect(host='ec2-52-201-66-148.compute-1.amazonaws.com', database='d44ns4ruujn4nq', port=5432,
                                user='ub5debmb55aodh', password='pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163')
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")
    
    return conn

def get_insert_query(tablename, fields):
    num_fields = len(fields)
    format = "(%s)" if num_fields == 1 else "(%s" + ",%s" * (num_fields - 1) + ")"
    rowId = fields[-4]

    sql_insert = "INSERT INTO " + tablename + " VALUES" + format

    return sql_insert

def prevent_repeat_inserts_prefix(tablename, row_id):
    return  "IF NOT EXISTS (SELECT * FROM " + tablename + " WHERE " + \
             "rowID = '" + row_id + "')"

def wrap_query(tablename, insert_query, row_id):
    query_prefix = prevent_repeat_inserts_prefix(tablename, row_id)

    return "DO\n$do$\nBEGIN\n" + "\t" + query_prefix + " THEN\n\t\t" + \
                    insert_query + ";\n\tEND IF;\nEND\n$do$"

# ***** connect to the db and api *******
def import_from_api_to_heroku(fields, tablename, primary_key, create_table_query="", rewrite_table=False):

    client = Socrata(
        "data.lacounty.gov",
        app_token='8uMOnLx6S823qlm58la47e6Pd', # tech equity token for socrata api access
        timeout=1000
    )

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

    num_records = client.get_all('9trm-uz8i', select="count(*)")
    num_records = int(next(num_records).get("count"))
    print("Total of ", num_records, " to import")

    ### page size = 1000 -> 33k rows/min
    ### page size = 25k -> 40k rows/40 sec
    ### page size = 50k -> 50k rows/38 sec
    offset = 0
    limit = 25000

    try:
        print("Inserting data")

        while(offset < num_records):
            data_generator = client.get('9trm-uz8i', select=cols_as_string,
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

def clean_parcelData():
    #modeled after https://www.postgresqltutorial.com/postgresql-python/delete/
    conn = None
    #we can keep track of how many rows we're deleting 
    # to see if our cleaning method is helpful
    try:

        conn = pg.connect(host='ec2-52-201-66-148.compute-1.amazonaws.com', database='d44ns4ruujn4nq', port=5432,
                                user='ub5debmb55aodh', password='pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163')
        cur = conn.cursor()
        #deleting rows based on anna's work 
        cur.execute("DELETE FROM rawParcelData WHERE GeneralUseType = 'Residential' ")
        cur.execute("DELETE FROM rawParcelData WHERE GeneralUseType is null")
        cur.execute("DELETE FROM rawParcelData WHERE isTaxableParcel? = 'N' ")
        cur.execute("DELETE FROM rawParcelData WHERE ZIPcode5 is null")
        cur.execute("DELETE FROM rawParcelData WHERE RollYear is null")
        cur.execute("DELETE FROM rawParcelData WHERE LandBaseYear is null")
        cur.execute("DELETE FROM rawParcelData WHERE LandValue is null")
        cur.execute("DELETE FROM rawParcelData WHERE SQFTmain = '0' ")
        cur.execute("DELETE FROM rawParcelData WHERE rowID is null")
        cur.execute("DELETE FROM rawParcelData WHERE Location 1 = '(0.0°, 0.0°)'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LON = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT = '0'")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT is null")
        cur.execute("DELETE FROM rawParcelData WHERE CENTER_LAT is null")
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
