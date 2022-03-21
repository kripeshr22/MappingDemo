from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import knn_metric as mt
import os, sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

NUM_NEIGHBORS = 10
WEIGHTS = 'uniform'        # default = 'uniform'
ALGORITHM = 'auto'         # default - 'auto'
METRIC = mt.custom_metric  # default = 'minkowski'


def main():
    # Create dataframes
    select_cols = ['center_lat', 'center_lon', 'propertyusecode', 'landvalue','sqftmain']
    tablename = 'cleanlacountytable'

    train_df = get_data.get_past4y_df(tablename, select_cols)
    pred_df = get_data.get_distinct_df(tablename, select_cols)
    train_df = organize_data(train_df)
    pred_df = organize_data(pred_df)
    X_pred = pred_df.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1) # should we be removing sqft here? maybe not

    # Run ML model
    y_test, y_pred = create_ml_model(train_df)
    
    # Find error for test data
    print_errors(y_test, y_pred)
    make_plot(y_test, y_pred)

    # Create predictions for all unique properties
    #pred_df['predicted landvaluepersqft'] = knn.predict(X_pred)

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
    df= df[df['landvaluepersqft'] < 3000]

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

def create_ml_model(df):
    #--- Set independent and dependent variables ---#
    print('setting X and y')
    y = pd.DataFrame(df['landvaluepersqft'])
    X = df.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1)

    print('starting machine learning now')
    # Split data randomly - 30% used for test data; 70% used for training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Create kNN Model
    knn= KNeighborsRegressor(n_neighbors=NUM_NEIGHBORS, weights = WEIGHTS, algorithm = ALGORITHM, metric = METRIC)
    knn.fit(X_train,y_train)
    y_pred = knn.predict(X_test)
    return y_test, y_pred

def make_plot(y, ypred):
    # Create a plot for errors vs landvaluepersqft 
    print('creating plot now')
    y_actual = np.array(y['landvaluepersqft'])
    size = ypred.size
    ypred = ypred.reshape((size,))
    errors = y_actual - ypred
    
    plt.figure()
    plt.scatter(y_actual, errors)
    plt.title('Prediction Error of Properties of Different Values')
    plt.xlabel('Land Value Per Sqft ($/sqft)')
    plt.ylabel('Error in Land Value Prediction ($/sqft)')
    plt.show()

def print_errors(y, ypred):
    print("For test properties")
    print("Mean predicted LV/sqft: ", ypred.mean())
    print("Mean actual LV/sqft: ", y['landvaluepersqft'].mean())
    print("St. Dev of predicted LV/sqft: ", ypred.std())
    print("St. Dev of actual LV/sqft: ", y['landvaluepersqft'].std())
    print("Mean error: ", sqrt(mean_squared_error(y,ypred)))

