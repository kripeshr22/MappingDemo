from math import sqrt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import knn_metric as mt
import os, sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)
import import_to_heroku

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data
import encode_zipcode

def main():
    # Create dataframes
    select_cols = ['ain','center_lat', 'center_lon', 'sqftmain', 'landbaseyear', 'landvalue']

    # train_df, est_df = encode_zipcode.main(select_cols = select_cols)
    train_df = get_data.get_past4y_df('cleanlacountytable', select_cols)
    est_df = get_data.get_distinct_df('laclean_pre2018_table', select_cols)
    train_df = organize_data(train_df)
    est_df = organize_data(est_df)
    
    # Replace landbaseyear and landvalue in the training dataframe with values from est_df
    est_df.rename(columns={'landbaseyear': 'prevvalueyear', 'landvalue': 'prevvalue'}, inplace = True)
    prevvalue_df = est_df[['prevvalueyear', 'prevvalue']].copy()
    train_df.drop(['landvalue'], axis=1, inplace=True)
    train_df = train_df.merge(prevvalue_df, how='inner', left_index=True, right_index=True)

    # Run ML model
    y_test, y_pred, y_test2021, y_pred2021, est_df = create_ml_model(train_df, est_df)
    
    # Find error for test data
    print("==== For all test data ====")
    print_errors(y_test, y_pred)
    make_plot(y_test, y_pred)

    print("==== For 2021 test data ====")
    print_errors(y_test2021, y_pred2021)
    make_plot(y_test2021, y_pred2021)

    # Create output df and upload to Heroku
    # outputdf = format_output_df(est_df)
    # import_to_heroku.create_and_insert_df(outputdf, 'la_rf_est_table')    

def organize_data(df):

    df = df.set_index('ain')

    for col in df:
        # Removes any row where column value is ''
        df= df[df[col]!= ''] 
        
        # Change data type to int and float
        df[col] = pd.to_numeric(df[col], downcast='integer')

    # Remove any row where any value is inf or nan
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    # Add land value per square foot to dataframe
    df['landvaluepersqft'] = df['landvalue']/df['sqftmain']
    
    df= df[df['sqftmain'] != 0]
    df= df[df['landvaluepersqft'] < 800]
   
    return df

def create_ml_model(df, est_df):

    # Split data randomly - 20% used for test data; 80% used for training data
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    df_test2021 = df_test[df_test['landbaseyear'] == 2021]

    #--- Set independent and dependent variables ---#

    y_train = df_train['landvaluepersqft']
    X_train = df_train.drop(['landvaluepersqft', 'landbaseyear'], axis=1)
    y_test = df_test['landvaluepersqft']
    X_test = df_test.drop(['landvaluepersqft', 'landbaseyear'], axis=1)
    y_test2021 = df_test2021['landvaluepersqft']
    X_test2021 = df_test2021.drop(['landvaluepersqft', 'landbaseyear'], axis=1)
    X_est = est_df.drop(['landvaluepersqft'], axis=1)

    # Create ML Model
    model = RandomForestRegressor(random_state= 42)
    model.fit(X_train,y_train)

    # Predictions for all test data
    y_pred = model.predict(X_test)

    # Just 2021 test data 
    y_pred2021 = model.predict(X_test2021)

    # Make predictions for all unique properties
    est_df['est_lvpersqft'] = model.predict(X_est)
    est_df['est_lv'] = est_df['est_lvpersqft']* est_df['sqftmain']

    return y_test, y_pred, y_test2021, y_pred2021, est_df

def make_plot(y, ypred):
    # Create a plot for errors vs landvaluepersqft 
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
    print("R^2 : ", r2_score(y, ypred))

def format_output_df(df):
    df.reset_index(inplace=True)
    outputdf = df[['ain', 'center_lat', 'center_lon', 'est_lv']].copy()
    # standardize column names
    outputdf.rename(columns={'ain': 'prop_id','center_lat': 'lat', 'center_lon': 'long','est_lv': 'estimated_value'}, inplace=True)
    # common formatting irregularities
    outputdf["estimated_value"] = outputdf["estimated_value"].round(2)
    outputdf['prop_id'] = outputdf['prop_id'].astype(str).apply(lambda x: x.replace('.0', ''))
    return outputdf

if __name__ == "__main__":
    main()
