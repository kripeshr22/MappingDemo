import pandas as pd

import os
import sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)
import import_to_heroku as imh

def get_df_from_heroku(tablename, cols=None):
    conn = imh.connect_to_heroku_db()
    if cols is None:
        df = pd.read_sql_query('select * from ' + tablename, con=conn)
    else:
        cols_as_string = ', '.join(cols)
        df = pd.read_sql_query('select ' + cols_as_string + ' from ' + tablename, con=conn)
    print("selected table from database")
    return df

def get_distinct_df(tablename, cols):
    conn = imh.connect_to_heroku_db()
    cols_as_string = ', '.join(cols)
    order = ' order by ain, landbaseyear desc'
    df = pd.read_sql_query('select distinct on (ain) ' + cols_as_string + ' from ' + tablename + order, con=conn)
    print("selected all distinct properties")
    return df

def get_past4y_df(tablename, cols=None):
    conn = imh.connect_to_heroku_db()
    if cols is None:
        df = pd.read_sql_query('select * from ' + tablename, con=conn)
    else:
        cols_as_string = ', '.join(cols)
        year_clause = ' where landbaseyear = \'2018\' OR landbaseyear = \'2019\' OR landbaseyear = \'2020\' OR landbaseyear = \'2021\''
        order = ' order by ain, landbaseyear desc'
        df = pd.read_sql_query('select distinct on (ain)' + cols_as_string + ' from ' + tablename + year_clause + order, con=conn)
    print("selected distinct properties from the past 4 years")
    return df

def get_test_df(tablename, cols, rows):
    conn = imh.connect_to_heroku_db()
    if cols is None:
        df = pd.read_sql_query('select * from ' + tablename, con=conn)
    else:
        cols_as_string = ', '.join(cols)
        test_list = []
        cursor = conn.cursor()
        for rowid in rows:
            cursor.execute('select ' + cols_as_string + ' from ' + tablename + ' where cast(rowid as double precision) = ' + rowid)
            test_list += [cursor.fetchone()]
        df = pd.DataFrame(test_list, columns = cols)
    print("selected test data from database")
    return df

def get_raw_df(county, cols=None):
    """get raw parcel dataset for county"""
    if county == "la":
        return get_df_from_heroku("rawlacountytable", cols)
    if county == "sf":
        return get_df_from_heroku("rawsfcountytable", cols)

def get_clean_df(county, cols=None):
    """get raw parcel dataset for county"""
    if county == "la":
        return get_df_from_heroku("cleanlacountytable", cols)

