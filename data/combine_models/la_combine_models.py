import os, sys
import pandas as pd
from sklearn.metrics import mean_squared_error

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)
import import_to_heroku

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

def main():
    # Pull data from manual estimation and random forest estimation tables
    comparisondf = create_comparisondf()

    # Compare average error for each type of estimation by zipcode and create df with final estimations
    combineddf = compare_error_by_zipcode(comparisondf)

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
    print('Finished fetching data')

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
    print('created comparisondf')

    return comparisondf

def compare_error_by_zipcode(df):
    ''' compare_error_by_zipcode calculates and compares the rmse for both types of 
        estimations in each zipcode. It then assigns the estimated value with the lower
        error rate to each property in that zipcode and sets is_manualest to 1 if the chosen
        estimation is manual, and 0 if it is from the rf model. 
        return: dataframe with columns ['prop_id','lat','long','zipcode','sqft','estimated_value','assessedin2021','is_manualest']
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
        else:
            df.loc[df['zipcode'] == zc, 'estimated_value'] = df.loc[df['zipcode'] == zc, 'est_value_rf']
            df.loc[df['zipcode'] == zc, 'is_manualest'] = False
    
    combineddf = df[['prop_id','lat','long','zipcode','estimated_value','assessedin2021','is_manualest']].copy()
    print('finished combining data')
    return combineddf

def upload_to_heroku(df):
    import_to_heroku.create_and_insert_df(df, 'la_final_est_table')
    print('uploaded final estimations to la_final_est_table')
