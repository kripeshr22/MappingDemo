import psycopg2 as pg
import csv


""" 
    Finds the worst offenders, and similar properties to the worst offenders, and outputs 
    that information into the excel spreadsheet case_studies.csv
"""
def main():
    host = 'ec2-52-201-66-148.compute-1.amazonaws.com'
    database='d44ns4ruujn4nq'
    port=5432
    user='ub5debmb55aodh'
    password='pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163'
    tablename = 'cleanLACountyTable'
    
    # connect to the database
    conn = connect_to_db(host, database, user, password)
    cur = conn.cursor()

    # get worst offenders
    results = find_worst_offenders(cur, tablename)

    # rows is a 2D array containing the rows for the excel spreadsheet
    rows = []
    # add column names
    rows += [['rowid', 'address', 'specificusetype', 'landvalue', 'sqftmain', 'lat', 'lon', 'landval/sqft']]

    for i in range(len(results)):
        result = results[i]

        # get similar properties
        similar = find_similar_properties(result[4], result[5], result[6], result[2], cur, tablename)

        # only add worst offender that have a similar properties
        if len(similar) > 1:
            # adds result to rows (including landvalue/sqft) 
            rows += [result + (str(float(result[3])/float(result[4])),)]

            # add each similar property to rows, then add an empty row
            for r in similar:
                if r != result:
                    rows += [r + (str(float(r[3])/float(r[4])),)]
            rows += [['']]
    
    # add the rows to excel sheet called case_studies.csv
    with open('case_studies.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerows(rows)
    print("results in case_studies.csv")

    if (conn):
        cur.close()
        conn.close()
        print("Connection to database closed.")

""" 
    connects to database 
"""
def connect_to_db(host, database, user, password):
    try:
        conn = pg.connect(host=host, database=database, user=user, password=password)
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")

    # cursor
    return conn

  
""" 
    Finds properties similar to the given property
    Takes in the sqft, latitude, longitude, and use code of the original property, and also the cur 
    and tablename
    Finds properties with a similar latitude and longitude, a similar sqft, the same property use code
    (so these are buildings used for similar things), and finds a max of five similar properties 
    Also picks out the properties that have the highest landvalue/sqft ratios
    Returns a list of touples of the similar properties
    Each touple contains: (rowid, address, usecode, landvalue, sqft, center_lat, center_lon)
"""
def find_similar_properties(sqftmain, lat, lon, code, cur, tablename):
    # margins of error for sqft, lat, lon
    # super high now because not many properties were showing up 
    sqft_error = 1500
    # this is about a mile
    lat_error = 0.015
    lon_error = 0.018

    # selects rows of similar lat/lon/sqft (based on the error margins above), with the same property
    # use code, and with roll year 2021
    # gets a max of 5 similar properties, and the ones chosen have the highest landvalue/sqft ratio
    cur.execute(
        "SELECT rowid, propertylocation, propertyusecode, landvalue, sqftmain, center_lat, \
        center_lon FROM " + tablename + " WHERE CAST(center_lat AS DOUBLE PRECISION) > " 
        + str(float(lat) - lat_error) + " AND CAST(center_lat AS DOUBLE PRECISION) < " 
        + str(float(lat) + lat_error) + " AND CAST(center_lon AS DOUBLE PRECISION) > " 
        + str(float(lon) - lon_error) +  " AND CAST(center_lon AS DOUBLE PRECISION) < " 
        + str(float(lon) + lon_error) +  " AND propertyusecode = '" + code + "'" +
        " AND CAST(sqftmain AS DOUBLE PRECISION) > " + str(int(sqftmain) - sqft_error) 
        + " AND CAST(sqftmain AS DOUBLE PRECISION) < " + str(int(sqftmain) + sqft_error) 
        + "AND rollyear='2021' ORDER BY (CAST(landvalue AS DOUBLE PRECISION)/CAST(sqftmain  \
            AS DOUBLE PRECISION)) DESC limit 5")
    
    results = cur.fetchall()
    return results
    


""" 
    Find the 'worst offenders' 
    Currently, does this by querying the database for properties with the worst landvalue/sqft ratio
    We could change this later to use ML model to find worst offenders
    Method takes in cur and table name
    Returns a list of touples (one for each worst offender) 
    Each touple contains: (rowid, address, usecode, landvalue, sqft, center_lat, center_lon)
    possible TODO - could change later to use ML
"""
def find_worst_offenders(cur, tablename):
    # query database - select these columns from tablename from the year 2021, order by the 
    # landvale to sqft ratio in ascending order (worst ratio is first), and get the top 20 offenders
    cur.execute("Select rowid, propertylocation, propertyusecode, landvalue, sqftmain, center_lat, \
        center_lon from " + tablename + " where rollyear='2021' ORDER BY (CAST(landvalue AS DOUBLE \
        PRECISION)/CAST(sqftmain AS DOUBLE PRECISION)) ASC limit 100")

    # get the results and return
    results = cur.fetchall()
    return results

