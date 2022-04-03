from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix
import csv
import numpy as np
import pandas as pd
import knn_metric as mt
import matplotlib.pyplot as plt
import os, sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

NUM_NEIGHBORS = 11
WEIGHTS = 'uniform'        # default = 'uniform'
ALGORITHM = 'auto'         # default - 'auto'
METRIC = mt.custom_metric  # default = 'minkowski'

# case studies for test data
rows = ['20218343001022', '20218341002019', '20218326006011', '20218340027025', '20218335013012', '20218342002020', 
        '20214288014002', '20214291018015', '20214291015027', '20214288003023', '20214288002044', '20214291011012']
        #'20216211005003', '20216204021019', '20216323025055', '20216208001023', '20216209015040', '20216202002028'

def main():
    select_cols = ['center_lat', 'center_lon', 'propertyusecode', 'landbaseyear', 'landvalue','sqftmain']
    tablename = 'cleanlacountytable'
    df = get_data.get_test_df(tablename, select_cols, rows)
    df = organize_data(df)
    nb = find_nbdistances(df)

    # Print data into csv; adapted from https://www.discoverbits.in/2152/how-to-save-a-python-csr_matrix-as-a-csv-file
    nb_df = pd.DataFrame(csr_matrix.todense(nb))
    csv_file = "nbdistances.csv"
    print("Write data to a CSV file ", csv_file)
    nb_df.to_csv(csv_file, index=False, header=None)

def organize_data(df):

    #--- Preliminary cleaning ---#
    for col in df:
        # Removes any row where column value is ''
        df= df[df[col]!= ''] 
        
        # Change data type to int and float
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # Add land value per square foot to dataframe
    df['landvaluepersqft'] = df['landvalue']/df['sqftmain']
    
    df= df[df['sqftmain'] != 0]
    df= df[df['landvaluepersqft'] < 1000]
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    
    print('finished cleaning data')
    return df

def find_nbdistances(df):
    print('setting X and y')
    y = pd.DataFrame(df['landvaluepersqft'])
    X = df.drop(['landvaluepersqft'], axis=1)

    print('starting machine learning now')
    
    # Create kNN Model
    knn= KNeighborsRegressor(n_neighbors=NUM_NEIGHBORS, weights=WEIGHTS, algorithm=ALGORITHM, metric=METRIC, p=2)
    knn.fit(X,y)
    dist_matrix = knn.kneighbors_graph(X=None, n_neighbors=None, mode='distance')
    return dist_matrix
    #nb, ind = knn.kneighbors(X=None, n_neighbors=None, return_distance=True)
    #return nb, ind

    

def run_ml_model(df):
    #--- Set independent and dependent variables ---#
    print('setting X and y')
    y = pd.DataFrame(df['landvaluepersqft'])
    X = df.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1)

    print('starting machine learning now')
    # Split data randomly - 30% used for test data; 70% used for training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Create kNN Model
    knn= KNeighborsRegressor(n_neighbors=NUM_NEIGHBORS, weights = WEIGHTS, algorithm = ALGORITHM, metric = METRIC)
    knn.fit(X_train,y_train)
    print('created knn model')

    # Create predictions for test data
    y_pred = knn.predict(X_test)
    print('made predictions for test data, now moving on to assess data')

    # Create a dataframe that contains all columns, but only rows where landbaseyear is 2021
    df_assess = df.copy()
    df_assess = df_assess[df_assess['landbaseyear'] == 2021]

    # Set dependent and independent variables for the properties that were assessed in 2021 (y_assess_pred), 
    y_assess = pd.DataFrame(df_assess['landvaluepersqft'])
    X_assess = df_assess.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1)

    # Make predictions for the properties that were assessed in 2021
    y_assess_pred = knn.predict(X_assess)

    print('made predictions for assess data, returning y_assess and y_assess_pred now')
    return y_assess, y_assess_pred, y_test, y_pred

def make_plot(y, ypred):
    # Create a plot for errors vs landvaluepersqft for properties assessed in 2021
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

def print_errors(y, ypred, is_2021: bool):
    if is_2021:
        print("For properties assessed in 2021")
    else:
        print("For test properties")
    print("Mean predicted LV/sqft: ", ypred.mean())
    print("Mean actual LV/sqft: ", y['landvaluepersqft'].mean())
    print("St. Dev of predicted LV/sqft: ", ypred.std())
    print("St. Dev of actual LV/sqft: ", y['landvaluepersqft'].std())
    print("Mean error: ", sqrt(mean_squared_error(y,ypred)))

