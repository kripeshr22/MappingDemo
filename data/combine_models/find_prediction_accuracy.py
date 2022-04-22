import os, sys
import pandas as pd
import numpy as np

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

BY_ZIPCODE = False # Boolean value which determines which table the function calculates the error for

def main():
    ''' 
    find_prediction_accuracy.py finds the average relative error for a given final 
    estimation table (either la_final_est_byzipcode or la_final_est_byquantile)
    '''
    if BY_ZIPCODE:
        tablename = 'la_final_est_byzipcode'
    else:
        tablename = 'la_final_est_byquantile'
    cols = ['recorded_value','estimated_value','assessedin2021']
    df = get_data.get_df_from_heroku(tablename, cols)
    df2021 = df[df['assessedin2021']==True].copy()

    # Calculate the absolute error for each property
    df2021['abs_err'] = abs(df2021['recorded_value']-df2021['estimated_value'])
    mean_rel_err = df2021['abs_err'].sum()/df2021['recorded_value'].sum()
    print(mean_rel_err)

if __name__ == "__main__":
    main()
