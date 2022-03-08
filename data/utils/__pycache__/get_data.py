import import_to_heroku as imh
import pandas as pd

import os
import sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)


def get_df_from_heroku(tablename):
    conn = imh.connect_to_heroku_db()
    df = pd.read_sql_query('select * from ' + tablename, con=conn)
    print("selected table from database")
    return df


def get_raw_df(county):
    """get raw parcel dataset for county"""
    if county == "la":
        return get_df_from_heroku("rawlacountytable")
    if county == "sf":
        return get_df_from_heroku("rawsfcountytable")
