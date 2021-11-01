import psycopg2
from create_table import create_table_query
import os
from sodapy import Socrata

# tech equity app token for socrata api access
client = Socrata(
    "data.lacounty.gov",
    app_token='8uMOnLx6S823qlm58la47e6Pd',
    timeout=1000
)


# print(data[0])

# ***** connect to the db *******
try:
    conn = psycopg2.connect(database='parcelDatabase', user=os.getenv("USER"), password=os.getenv("PASSWORD"))
    print("successfully connected to database")
except:
    print("I am unable to connect to the database")

# cursor
cur = conn.cursor()


# all columns
fields = [
        'ain',
        'situszip',
        # 'taxratearea_city',
        # 'rollyear',
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
        'istaxableparcel',
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


# uncomment the following line if schema has been updated:
# cur.execute("DROP TABLE IF EXISTS rawParcelTable")

# rewriting entire table for now
cur.execute("DROP TABLE IF EXISTS rawParcelTable")
cur.execute(create_table_query)
print("created table. connecting to api")

cols_as_string = ", ".join(fields)
data_generator = client.get('9trm-uz8i', select="distinct " + cols_as_string,
                                usecodedescchar1="Commercial", istaxableparcel="Y", 
                                limit=100000)

print("successfully got data generator from api endpoint")

rows = 0
for row in data_generator:
    # insert into table
    my_data = [row.get(field, "") for field in fields]
    insert_query = "INSERT INTO rawParcelTable VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"

    # -- uncomment line to show error message --
    cur.execute(insert_query, tuple(my_data))
    rows = rows + 1

    # -- show problem row, prevent error message --
    # try:
    #     cur.execute(insert_query, tuple(my_data))
    # except:
    #     print(my_data)
    #     break
print(rows)

print("further cleaning the data")
cur.execute("UPDATE rawParcelTable SET sqftmain = REPLACE(sqftmain, ',', '')")
cur.execute(
    "UPDATE rawParcelTable SET roll_landvalue = REPLACE(roll_landvalue, ',', '')")
cur.execute("DELETE FROM rawParcelTable WHERE center_lon = '0'")
cur.execute("DELETE FROM rawParcelTable WHERE center_lat = '0'")
cur.execute("DELETE FROM rawParcelTable WHERE roll_landbaseyear = '0'")
conn.commit()

print("closing cursor and connection")
# close the cursor
cur.close()

# close the connection
conn.close()

