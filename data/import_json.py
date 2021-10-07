import json, urllib.request, requests
import psycopg2
from psycopg2.extras import execute_values
from create_table import create_table_query

# Retrieve Json Data from Within API

url = "https://data.lacounty.gov/resource/9trm-uz8i.json"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

# print(data[0])

# ***** connect to the db *******
try:
    conn = psycopg2.connect(database='parceldatabase', user='techequity', password='clinic')
    print("successfully connected to database")
except:
    print("I am unable to connect to the database")

# cursor
cur = conn.cursor()


# all columns
fields = [
    'situszip', 
    # 'taxratearea_city', 
    'ain', 
    'rollyear', 
    # 'taxratearea', 
    # 'assessorid', 
    # 'propertylocation', 
    # 'usetype', 
    # 'usecode', 
    'usecodedescchar1', #general use type: residential or commercial
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
    'roll_landbaseyear', 
    'roll_impvalue', 
    'roll_impbaseyear',
    'roll_totlandimp', 
    # 'roll_homeownersexemp', 
    # 'roll_realestateexemp', 
    # 'roll_fixturevalue', 
    # 'roll_fixtureexemp', 
    # 'roll_perspropvalue', 
    # 'roll_perspropexemp', 
    'istaxableparcel', 
    'roll_totalvalue', 
    # 'roll_totalexemption', 
    'nettaxablevalue', 
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
    'rowid', 
    'center_lat', 
    'center_lon',
    # 'location_1',
]

# uncomment the following line if schema has been updated:
# cur.execute("DROP TABLE IF EXISTS rawParcelTable")

cur.execute(create_table_query)
for row in data:
    my_data = [row[field] for field in fields]
    insert_query = "INSERT INTO rawParcelTable VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try: 
        cur.execute(insert_query, tuple(my_data))
    except:
        print(my_data)
        break
    conn.commit()

# close the cursor
cur.close()

# close the connection
conn.close()
