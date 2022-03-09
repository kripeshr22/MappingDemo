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

