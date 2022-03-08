import pandas as pd
import category_encoders as ce
from import_scripts.import_to_heroku import *


def main(encode="one_hot"):
    tablename = 'cleanlacountytable'
    encode_col = 'zipcode5'

    conn = connect_to_heroku_db()
    df = get_dataframe(conn, tablename)

    if encode == "hash":
        return encode_hash(df, 5, encode_col)
    if encode == "one_hot":
        return encode_one_hot(df, encode_col)

def get_dataframe(conn, tablename):
    df = pd.read_sql_query('select * from ' + tablename, con=conn)
    print("selected table from database")
    return df


def encode_hash(df, count, encode_col):
    encoder_purpose = ce.HashingEncoder(n_components=count, cols=[encode_col])
    hashlabels = encoder_purpose.fit_transform(df)
    return hashlabels


def encode_one_hot(df, encode_col):
    enc = ce.OneHotEncoder(cols=[encode_col], return_df=True)
    onehotlabels = enc.fit_transform(df)
    return onehotlabels





