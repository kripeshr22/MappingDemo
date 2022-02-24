# import numpy as np
import pandas as pd
import psycopg2
import category_encoders as ce
import db_config
from import_scripts.import_to_heroku import *


def main(encode="one_hot"):
    # conn = get_conn(HOST_NAME, DB_NAME, USERNAME, PW)
    tablename = 'cleanlacountytable'
    encode_col = 'zipcode5'

    conn = connect_to_heroku_db()
    df = get_dataframe(conn, tablename, encode_col)

    if encode == "hash":
        return encode_hash(df, 5)
    if encode == "one_hot":
        return encode_one_hot(df)

def get_dataframe(conn, tablename, column):
    df = pd.read_sql_query('select distinct ' + column + ' from ' + tablename, con=conn)
    print("selected table from database")
    return df

def encode_hash(df, count):
    encoder_purpose = ce.HashingEncoder(n_components=count, cols=[COLUMN])
    hashlabels = encoder_purpose.fit_transform(df)
    return hashlabels

def encode_one_hot(df):
    enc = ce.OneHotEncoder(cols=[COLUMN], return_df=True)
    onehotlabels = enc.fit_transform(df)
    return onehotlabels





