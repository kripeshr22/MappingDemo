from pandas.core import groupby
import psycopg2
from create_table import create_table_query
from sodapy import Socrata
import pandas as pd
from utils import profile 

# ***** connect to the db and api *******
@profile
def import_to_heroku():

    # tech equity app token for socrata api access
    client = Socrata(
        "data.lacounty.gov",
        app_token='8uMOnLx6S823qlm58la47e6Pd',
        timeout=1000
    )

    # updated to standard-0 heroku db
    try:
        conn = psycopg2.connect(host='ec2-52-201-66-148.compute-1.amazonaws.com', database='d44ns4ruujn4nq', port=5432,
                                user='ub5debmb55aodh', password='pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163')
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")

        # all columns with unused cols commented out


    # just getting land values for now -> will add in improvement value later
    fields = [
        'situszip',
        # 'taxratearea_city',
        # 'ain',
        'rollyear',
        # 'taxratearea',
        # 'assessorid',
        # 'propertylocation',
        # 'usetype',
        # 'usecode',
        'usecodedescchar1',  # general use type: residential or commercial
        # 'usecodedescchar2',
        # 'usecodedescchar3',
        # 'usecodedescchar4',
        # 'totbuildingdatalines',
        # 'yearbuilt',
        # 'effectiveyearbuilt',
        'sqftmain',
        # 'bedrooms',
        # 'bathrooms',
        # 'units',
        # 'recordingdate',
        'roll_landvalue',
        'roll_landbaseyear',  # this gets updated when change in ownership
        # 'roll_impvalue',
        # 'roll_impbaseyear',
        # 'roll_totlandimp',
        # 'roll_homeownersexemp',
        # 'roll_realestateexemp',
        # 'roll_fixturevalue',
        # 'roll_fixtureexemp',
        # 'roll_perspropvalue',
        # 'roll_perspropexemp',
        # 'istaxableparcel',
        # 'roll_totalvalue',
        # 'roll_totalexemption',
        # 'nettaxablevalue',
        # 'parcelclassification',
        # 'adminregion',
        # 'cluster',
        # 'parcelboundarydescription',
        # 'situshouseno',
        # 'situsfraction',
        # 'situsdirection',
        # 'situsstreet',
        # 'situsunit',
        # 'situscity',
        # 'situszip5',
        # 'rowid',
        'center_lat',
        'center_lon',
        # 'location_1',
    ]


    # cursor
    cur = conn.cursor()



    # rewriting entire table for now
    cur.execute("DROP TABLE IF EXISTS rawParcelTable")
    cur.execute(create_table_query)
    print("created table. connecting to api")


    # Retrieve Json Data from API endpoint
    cols_as_string = ", ".join(fields)
    query = "SELECT " + cols_as_string + "DISTINCT ON(ain) " + \
        "ORDER BY `rollyear` DESC"

    data_generator = client.get_all('9trm-uz8i', select=cols_as_string + ", distinct ain", 
        usecodedescchar1="Commercial", staxableparcel="Y", order="rollyear DESC")

    print("successfully got data generator from api endpoint")

    # counter = 0
    # for r in data_generator:
    #     if counter == 10:
    #         break
    #     counter = counter + 1
    #     print(r)

    fields = ['ain'] + fields
    for row in data_generator:
        # insert into table
        my_data = [row.get(field, "") for field in fields]
        insert_query = "INSERT INTO rawParcelTable VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # -- uncomment line to show error message -- 
        cur.execute(insert_query, tuple(my_data)) 

        # -- show problem row, prevent error message --
        # try: 
        #     cur.execute(insert_query, tuple(my_data))
        # except:
        #     print(my_data) 
        #     break
        conn.commit()

    print("closing cursor and connection")
    # close the cursor
    cur.close()

    # close the connection
    conn.close()
