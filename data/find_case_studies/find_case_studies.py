import psycopg2 as pg
import psycopg2.extras
import numpy as np
import pandas as pd

""" Change tablename to whatever the name of the table is,
 and the inputs should be strings containing the streetname
 and the specific use type.
"""

def main(situsstreet, usecodedescchar2):
    host = 'ec2-52-201-66-148.compute-1.amazonaws.com'
    database='d44ns4ruujn4nq'
    port=5432
    user='ub5debmb55aodh'
    password='pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163'
    tablename = 'rawLACountyTable'
    
    conn = connect_to_db(host, database, user, password)
    cur = conn.cursor()

    find_similar_properties(situsstreet, usecodedescchar2)

    if (conn):
        cur.close()
        conn.close()
        print("Connection to database closed.")

def connect_to_db(host, database, user, password):
    try:
        conn = pg.connect(host=host, database=database, user=user, password=password)
        print("successfully connected to database")
    except:
        print("I am unable to connect to the database")

    # cursor
    return conn

def find_similar_properties(situsstreet, usecodedescchar2):
    cur.execute('SELECT * FROM ' + tablename + ' WHERE situsstreet = ' + situsstreet + ' AND usecodedescchar2 = ' + usecodedescchar2)
   

