from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
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

# NUM_NEIGHBORS = 10
# WEIGHTS = 'uniform'        # default = 'uniform'
# ALGORITHM = 'auto'         # default - 'auto'
# METRIC = mt.custom_metric  # default = 'minkowski'


def main():
    # Create dataframes
    # select_cols = ['ain','center_lat', 'center_lon', 'propertyusecode', 'landbaseyear', 'landvalue','sqftmain']
    select_cols = ['landbaseyear', 'landvalue','sqftmain']
    tablename = 'cleanlacountytable'

    train_df = get_data.get_past4y_df(tablename, select_cols)
    pred_df = get_data.get_distinct_df(tablename, select_cols)
    train_df = organize_data(train_df)
    pred_df = organize_data(pred_df)
    
    # Run ML model
    y_test, y_pred, y_test2021, y_pred2021 = create_ml_model(train_df)
    
    # Find error for test data
    print("==== For all test data ====")
    print_errors(y_test, y_pred)
    make_plot(y_test, y_pred)

    print("==== For 2021 test data ====")
    print_errors(y_test2021, y_pred2021)
    make_plot(y_test2021, y_pred2021)

    # Create predictions for all unique properties
    #pred_df['predicted landvaluepersqft'] = knn.predict(X_pred)

def organize_data(df):
    for col in df:
        # Removes any row where column value is ''
        df= df[df[col]!= ''] 
        
        # Change data type to int and float
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # Add land value per square foot to dataframe
    df['landvaluepersqft'] = df['landvalue']/df['sqftmain']
    
    df= df[df['sqftmain'] != 0]
    df= df[df['landvaluepersqft'] < 800]

    # Remove any row where any value is inf or nan
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    print('finished cleaning data')
    return df

def create_ml_model(df):

    # Split data randomly - 20% used for test data; 80% used for training data
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df_test2021 = df_test[df_test['landbaseyear'] == 2021]

    #--- Set independent and dependent variables ---#
    print('setting X and y')
    y_train = df_train['landvalue']
    X_train = df_train.drop(['landvaluepersqft', 'landvalue', 'landbaseyear'], axis=1)
    y_test = df_test['landvalue']
    X_test = df_test.drop(['landvaluepersqft', 'landvalue', 'landbaseyear'], axis=1)
    y_test2021 = df_test2021['landvalue']
    X_test2021 = df_test2021.drop(['landvaluepersqft', 'landvalue', 'landbaseyear'], axis=1)


    # Create ML Model
    print('starting machine learning now')
    # knn= KNeighborsRegressor(n_neighbors=NUM_NEIGHBORS, weights = WEIGHTS, algorithm = ALGORITHM, metric = METRIC)
    # knn.fit(X_train,y_train)
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)

    # Predictions for all test data
    y_pred = rf.predict(X_test)

    # Just 2021 test data 
    y_pred2021 = rf.predict(X_test2021)

    # Convert to landvaluepersqft from landvalue
    y_test /= X_test['sqftmain']
    y_pred /= X_test['sqftmain']
    y_test2021 /= X_test2021['sqftmain']
    y_pred2021 /= X_test2021['sqftmain']
    #import ipdb; ipdb.set_trace()

    return y_test, y_pred, y_test2021, y_pred2021

def make_plot(y, ypred):
    # Create a plot for errors vs landvaluepersqft 
    print('creating plot now')
    #y_actual = np.array(y)
    #size = ypred.size
    #ypred = ypred.reshape((size,))
    errors = y - ypred
    
    plt.figure()
    plt.scatter(y, errors)
    plt.title('Prediction Error of Properties of Different Values')
    plt.xlabel('Land Value Per Sqft ($/sqft)')
    plt.ylabel('Error in Land Value Prediction ($/sqft)')
    plt.show()

def print_errors(y, ypred):
    print("For test properties")
    print("Mean predicted LV/sqft: ", ypred.mean())
    print("Mean actual LV/sqft: ", y.mean())
    print("St. Dev of predicted LV/sqft: ", ypred.std())
    print("St. Dev of actual LV/sqft: ", y.std())
    print("Mean error: ", sqrt(mean_squared_error(y,ypred)))

