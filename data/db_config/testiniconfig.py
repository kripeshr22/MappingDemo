# This file is to test the .ini and config.py files
# Currently set up to work in python files in subfolders of data eg. find_case_studies and import_scripts
# Mariesa Teo
import psycopg2
from sodapy import Socrata

# this import section adapted from https://csatlas.com/python-import-file-module/#relative_path
import os
import sys
current_dir = os.path.dirname( __file__ )
config_dir = os.path.join( current_dir, '..', 'db_config' )
sys.path.append( config_dir )
import config as cf

def main():
    params = cf.config()
    conn = psycopg2.connect(**params)
    print("I am connected to the database")

    cur = conn.cursor()

# Print the number of rows in this table to prove that we are connecting to the database
    cur.execute('SELECT count(*) from cleanlacountytable;', [])
    results = cur.fetchone()
    print(results)

    #close cursor and database connection
    cur.close()
    conn.close()
    print("finished")

