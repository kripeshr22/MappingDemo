import os, sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)
import import_to_heroku

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

BY_ZIPCODE = False  # Boolean value: True if calculating error by zipcode, False if by quantile

def main():
    # Pull data from manual estimation and random forest estimation tables
    comparisondf = create_comparisondf()

    # Compare average error for each type of estimation by zipcode/quantile and create df with final estimations
    if BY_ZIPCODE:
        combineddf = compare_error_by_zipcode(comparisondf)
    else:
        combineddf = compare_error_by_quantile(comparisondf)

    # Upload df to Heroku
    upload_to_heroku(combineddf)

def create_comparisondf():
    ''' create_comparisondf pulls data from la_manual_est_table and la_rf_est_table to 
        create a pandas dataframe that can be used to compare our manual estimations 
        and random forest estimations for property values
        return: dataframe with columns
        ['prop_id','recorded_value','est_value_manual','est_value_rf','lat','long', 'zipcode','assessedin2021']
    '''
    # Fetch all necessary data from Heroku
    manual_df = get_data.get_df_from_heroku('la_manual_est_table')
    rf_df = get_data.get_df_from_heroku('la_rf_est_table')
    assessedin2021_df = get_data.get_2021_df('cleanlacountytable', ['ain', 'landbaseyear'])

    # Make comparisondf
    comparisondf = pd.merge(manual_df, rf_df, how='outer', on='prop_id')
    comparisondf['assessedin2021'] = comparisondf['prop_id'].isin(assessedin2021_df['ain'])
    comparisondf.drop(['lat_y', 'long_y', 'value_diff'], axis=1, inplace=True)
    comparisondf.rename(columns={'lat_x':'lat', 'long_x':'long','estimated_value_x':'est_value_manual','estimated_value_y':'est_value_rf','zipcode5':'zipcode'}, inplace=True)
    
    # Handle money columns
    for col in ['recorded_value','est_value_manual','est_value_rf']:
        comparisondf.loc[comparisondf[col].isnull()] = 0
        comparisondf[col] = comparisondf[col].str.replace(',','')
        comparisondf[col] = comparisondf[col].str.replace('\$','')
        comparisondf[col] = pd.to_numeric(comparisondf[col])

    return comparisondf

def compare_error_by_zipcode(df):
    ''' compare_error_by_zipcode calculates and compares the rmse for both types of 
        estimations in each zipcode. It then assigns the estimated value with the lower
        error rate to each property in that zipcode and sets is_manualest to 1 if the chosen
        estimation is manual, and 0 if it is from the rf model. 
        return: dataframe with columns 
        ['prop_id','lat','long','zipcode','sqft','address','recorded_value','estimated_value',
        'assessedin2021','is_manualest','rmse_byzipcode]
    '''
    zipcodes = df['zipcode'].unique()

    for zc in zipcodes:
        # Find rmse for each type of estimation
        df_zc2021 = df.loc[(df['zipcode'] == zc) & (df['assessedin2021'] == True)]
        manual_rmse = 0
        rf_rmse= 0
        if not df_zc2021.empty:
            manual_rmse = mean_squared_error(df_zc2021['recorded_value'],df_zc2021['est_value_manual'], squared=False)
            rf_rmse = mean_squared_error(df_zc2021['recorded_value'],df_zc2021['est_value_rf'], squared=False)

        # Compare rmse and set estimated_value and is_manualest
        if manual_rmse <= rf_rmse:
            df.loc[df['zipcode'] == zc, 'estimated_value'] = df.loc[df['zipcode'] == zc, 'est_value_manual']
            df.loc[df['zipcode'] == zc, 'is_manualest'] = True
            df.loc[df['zipcode'] == zc, 'rmse_byzipcode'] = manual_rmse
        else:
            df.loc[df['zipcode'] == zc, 'estimated_value'] = df.loc[df['zipcode'] == zc, 'est_value_rf']
            df.loc[df['zipcode'] == zc, 'is_manualest'] = False
            df.loc[df['zipcode'] == zc, 'rmse_byzipcode'] = rf_rmse
    
    combineddf = df[['prop_id','lat','long','zipcode','sqft','address','recorded_value','estimated_value','assessedin2021','is_manualest', 'rmse_byzipcode']].copy()
    overall_rmse = mean_squared_error(df.loc[df['assessedin2021'] == True, ['recorded_value']],df.loc[df['assessedin2021'] == True, ['estimated_value']], squared=False)
    mean_2021rv = df.loc[df['assessedin2021'] == True, 'recorded_value'].mean()
    print('overall rmse: ', overall_rmse)
    print('mean recorded_value for properties assessed in 2021: ', mean_2021rv)

    return combineddf

def compare_error_by_quantile(df):
    ''' compare_error_by_quantile calculates and compares the rmse for both types of 
        estimations for each tenth percentile. It then assigns the estimated value with the lower
        error rate to each property in that zipcode and sets is_manualest to 1 if the chosen
        estimation is manual, and 0 if it is from the rf model. 
        return: dataframe with columns 
        ['prop_id','lat','long','zipcode','sqft','address','recorded_value','estimated_value',
        'assessedin2021','is_manualest', 'rmse_byquantile]
    '''
    quantiles = df['recorded_value'].quantile(np.arange(0,1.1,0.1)).tolist()

    for i in range(len(quantiles)-1):
        # Find rmse for each type of estimation
        df_q2021 = df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]) & (df['assessedin2021'] == True)]
        manual_rmse = 0
        rf_rmse= 0
        if not df_q2021.empty:
            manual_rmse = mean_squared_error(df_q2021['recorded_value'],df_q2021['est_value_manual'], squared=False)
            rf_rmse = mean_squared_error(df_q2021['recorded_value'],df_q2021['est_value_rf'], squared=False)

        # Compare rmse and set estimated_value and is_manualest
        if manual_rmse <= rf_rmse:
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'estimated_value'] = df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'est_value_manual']
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'is_manualest'] = True
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'rmse_byquantile'] = manual_rmse
        else:
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'estimated_value'] = df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'est_value_rf']
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'is_manualest'] = False
            df.loc[(df['recorded_value'] > quantiles[i]) & (df['recorded_value'] <= quantiles[i+1]), 'rmse_byquantile'] = rf_rmse
    
    combineddf = df[['prop_id','lat','long','zipcode','sqft','address','recorded_value','estimated_value','assessedin2021','is_manualest', 'rmse_byquantile']].copy()
    overall_rmse = mean_squared_error(df.loc[df['assessedin2021'] == True, ['recorded_value']],df.loc[df['assessedin2021'] == True, ['estimated_value']], squared=False)
    mean_2021rv = df.loc[df['assessedin2021'] == True, 'recorded_value'].mean()
    print('overall rmse: ', overall_rmse)
    print('mean recorded_value for properties assessed in 2021: ', mean_2021rv)

    return combineddf

def upload_to_heroku(df):
    # Handle common formatting irregularities and errors in inserting into table
    df["estimated_value"] = df["estimated_value"].round(2)
    df["assessedin2021"] = df["assessedin2021"].astype(int)
    df["assessedin2021"] = df["assessedin2021"].astype('boolean')
    df["is_manualest"] = df["is_manualest"].fillna(False)
    
    # Upload
    if BY_ZIPCODE:
        import_to_heroku.create_and_insert_df(df, 'la_final_est_byzipcode')
        print('Uploaded final estimations to la_final_est_byzipcode')
    else:
        import_to_heroku.create_and_insert_df(df, 'la_final_est_byquantile')
        print('Uploaded final estimations to la_final_est_byquantile')

if __name__ == "__main__":
    main()
