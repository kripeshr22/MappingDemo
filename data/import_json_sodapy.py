import json, urllib.request, requests
import psycopg2
from psycopg2.extras import execute_values
from requests import api
from create_table import create_table_query
import pandas as pd
from sodapy import Socrata

# ***** connect to the db *******


client = Socrata(
    "data.lacounty.gov",
    username="nuqphmmgbdaxdi",
    password="ac659eafc14bad6a7c8d451e575d72c8b634f92b9ef09857af54633cebbc64b8",
    timeout=10
)
try:
    conn = psycopg2.connect(host='ec2-34-194-123-31.compute-1.amazonaws.com', database='dfvq9ek4f004sj', port=5432,
                            user='nuqphmmgbdaxdi', password='ac659eafc14bad6a7c8d451e575d72c8b634f92b9ef09857af54633cebbc64b8')
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

print(len(fields))
# uncomment the following line if schema has been updated:
cur.execute("DROP TABLE IF EXISTS rawParcelTable")
cur.execute(create_table_query)
print("created table. connecting to api")

# Retrieve Json Data from API endpoint
cols_as_string = ", ".join(fields)
# api_query = "?$limit=10000&$select=" + cols_as_string + \
#     "&$where=usecodedescchar1 = 'Commercial' AND istaxableparcel = 'Y'"
api_query = "?$limit=10000&$select=situszip" +\
    "&$where=istaxableparcel = 'Y'"

print(api_query)

url = "https://data.lacounty.gov/resource/9trm-uz8i.json" 
# response = urllib.request.urlopen(url)
# data = json.loads(response.read())
# print(data[0])

data = requests.get(url + api_query).json()

print(data[0])
# print(data)

print("data has ", len(data), " rows. inserting tuples into database")

for row in data:
    my_data = [row[field] for field in fields]
    insert_query = "INSERT INTO rawParcelTable VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try: 
        cur.execute(insert_query, tuple(my_data))
    except:
        print(my_data)
        break
    conn.commit()

print("closing cursor and connection")
# close the cursor
cur.close()

# close the connection
conn.close()
