# import numpy as np
import pandas as pd
import psycopg2
# from sklearn.preprocessing import OneHotEncoder, HashingEncoder
import category_encoders as ce


# Change these variables to suite local database and associated Postgresql username and password
HOST_NAME = 'ec2-52-201-66-148.compute-1.amazonaws.com'
DB_NAME = 'd44ns4ruujn4nq'
USERNAME = 'ub5debmb55aodh'
PW = 'pe6a56f3002c3f1181d1a34e26d9a90636fdd56e1156bf39a6b8ff158a49bf163'
TABLENAME = 'cleanlacountytable'
COLUMN = 'zipcode5'


def main():
    df = get_dataframe(HOST_NAME, DB_NAME, USERNAME, PW, TABLENAME, COLUMN)
    one_hot = encode_one_hot(df)
    hash = encode_hash(df)
    return {"one_hot": one_hot, "hash": hash}

def get_dataframe(host_name, db_name, username, pw, tablename, column):
    # Connect to local database
    try:
            conn = psycopg2.connect(
                host=host_name, database=db_name, port=5432, user=username, password=pw)
            print("successfully connected to database")
    except:
            print("I am unable to connect to the database")
    
    # Create dataframe
    df = pd.read_sql_query('select * from ' + tablename, con=conn)
    return df


def encode_hash(df):
    encoder_purpose = ce.HashingEncoder(n_components=300, cols=[COLUMN])
    hashlabels = encoder_purpose.fit_transform(df)
    return hashlabels

def encode_one_hot(df):
    enc = ce.OneHotEncoder(cols=[COLUMN], return_df=True)
    onehotlabels = enc.fit_transform(df)
    return onehotlabels





