import os, sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

def find_error_finalpreds(by_zipcode = True):
    ''' 
    find_error_finalpreds finds the average relative error for a given final 
    estimation table (either la_final_est_byzipcode or la_final_est_byquantile)
    by_zipcode is a bool which determines which table the function calculates the error for
    '''
    if by_zipcode:
        tablename = 'la_final_est_byzipcode'
    else:
        tablename = 'la_final_est_byquantile'
    cols = ['prop_id','recorded_value','estimated_value','assessedin2021']
    df = get_data.get_df_from_heroku(tablename, cols)
    df2021 = df[df['assessedin2021']==True].copy()

    # Calculate the absolute error for each property
    df2021['abs_err'] = abs(df2021['recorded_value']-df2021['estimated_value'])
    mean_rel_err = df2021['abs_err'].sum()/df2021['recorded_value'].sum()
    print(mean_rel_err) # Result: byzipcode- 0.69%; byquantile - 0.78%

def find_error_rf():
    ''' find_error_rf finds the average relative error for la_rf_est_table
    '''
    df_zc = get_data.get_df_from_heroku('la_final_est_byzipcode', ['prop_id','recorded_value','assessedin2021'])
    df_rf = get_data.get_df_from_heroku('la_rf_est_table', ['prop_id', 'estimated_value'])
    df = df_zc.merge(df_rf, how='outer', on='prop_id')
    df2021 = df[df['assessedin2021']==True].copy()

    # Convert estimated_value to a numeric type so we can do calculations with it
    df2021['estimated_value'] = df2021['estimated_value'].str.replace(',','')
    df2021['estimated_value'] = df2021['estimated_value'].str.replace('\$','')
    df2021['estimated_value'] = pd.to_numeric(df2021['estimated_value'])

    # Calculate the absolute error for each property
    df2021['abs_err'] = abs(df2021['recorded_value']-df2021['estimated_value'])
    # Calculate the average relative error
    mean_rel_err = df2021['abs_err'].sum()/df2021['recorded_value'].sum()
    print('Average Relative Error: ',mean_rel_err) # Result is 22.9%
    # Calculate RMSE
    rmse = mean_squared_error(df2021['recorded_value'], df2021['estimated_value'], squared = False)
    print('RMSE: ',rmse)
    # Calculate mean of 2021 property values
    mean_val = df2021['recorded_value'].mean()
    print('Mean Land Value: ', mean_val)
