from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import seaborn as sns

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

def main():
    # Create dataframes
    select_cols = ['ain','center_lat', 'center_lon', 'propertyusecode', 'landbaseyear', 'landvalue','sqftmain']
    tablename = 'cleanlacountytable'

    train_df = get_data.get_past4y_df(tablename, select_cols)
    pred_df = get_data.get_distinct_df(tablename, select_cols)
    train_df = organize_data(train_df)
    pred_df = organize_data(pred_df)

    print('===== For 2018-2021 Data =====')
    find_cutoff(train_df)   
    #plot_lvpersqft(train_df)
    # corr_matrix(train_df)

    print('===== For all unique data =====')
    find_cutoff(pred_df)  
    #plot_lvpersqft(pred_df)
    # corr_matrix(pred_df)


def organize_data(df):
    for col in df:
        # Removes any row where column value is ''
        df= df[df[col]!= ''] 
        
        # Change data type to int and float
        if col != 'propertyusecode':
            df[col] = pd.to_numeric(df[col], downcast='integer')

    # Add land value per square foot to dataframe
    df['landvaluepersqft'] = df['landvalue']/df['sqftmain']
    
    df= df[df['sqftmain'] != 0]
    # df= df[df['landvaluepersqft'] < 800]

    # Create a new column for each character in propertyusecode and turn any letters into numbers
    lettersToNumbers = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,
                    "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23,
                    "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30,
                    "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35, " ": 36, "*": 37}
    df['usecode1'] = df['propertyusecode'].astype(str).str[0]
    df['usecode2'] = df['propertyusecode'].astype(str).str[1]
    df['usecode3'] = df['propertyusecode'].astype(str).str[2]
    df['usecode4'] = df['propertyusecode'].astype(str).str[3]
    usecode_cols = ['usecode1', 'usecode2', 'usecode3', 'usecode4']
    for col in usecode_cols:
        for x in lettersToNumbers:
            df[col] = df[col].replace(x,lettersToNumbers[x])

    # Remove any row where any value is inf or nan
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    # concatenate back into propertyusecode
    df['propertyusecode'] = df['usecode1'].astype(str) + df['usecode2'].astype(str) + df['usecode3'].astype(str) + df['usecode4'].astype(str)
    df['propertyusecode'] = pd.to_numeric(df['propertyusecode'], downcast='integer')
    df.drop(usecode_cols, axis=1, inplace=True)
    
    print('finished cleaning data')
    return df

def find_cutoff(X):
    print('Proportion of data with landvaluepersqft below $400 is', len(X[X['landvaluepersqft']<400])/len(X))
    print('Proportion of data with landvaluepersqft below $600 is', len(X[X['landvaluepersqft']<600])/len(X))
    print('Proportion of data with landvaluepersqft below $800 is', len(X[X['landvaluepersqft']<800])/len(X))
    print('Proportion of data with landvaluepersqft below $900 is', len(X[X['landvaluepersqft']<900])/len(X))
    print('Proportion of data with landvaluepersqft below $1000 is', len(X[X['landvaluepersqft']<1000])/len(X))
    print('Proportion of data with landvaluepersqft below $3000 is', len(X[X['landvaluepersqft']<3000])/len(X))
    print('Proportion of data with landvaluepersqft below $5000 is', len(X[X['landvaluepersqft']<5000])/len(X))

def plot_lvpersqft(df):
    plt.figure()
    plt.hist(df['landvaluepersqft'], bins = 100, range = (0, 3000))
    plt.title('Distribution of Land Value Per Sqft')
    plt.xlabel('Land Value Per Sqft ($/sqft)')
    plt.show()

def corr_matrix(df):
    # get correlation matrix
    corr_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(15, 12))
    sns.heatmap(corr_matrix, vmax=0.8, square=True)
    plt.show()
