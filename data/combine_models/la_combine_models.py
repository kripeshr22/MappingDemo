import os, sys
import pandas as pd

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

    # Find average error for each type of estimation by zipcode
    comparisondf = find_error_by_zipcode(comparisondf)

    # Make df with final estimations
    combineddf = create_combineddf(comparisondf)

    # Upload df to Heroku
    upload_combineddf(combineddf)

def create_comparisondf():
    ''' create_comparisondf pulls data from la_manual_est_table and la_rf_est_table to 
        create a pandas dataframe that can be used to compare our manual estimations 
        and random forest estimations for property values
        return: dataframe with columns
        ['prop_id','lat','long','recorded_value','est_value_manual','est_value_rf','sqft','assessedin2021']
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
    comparisondf.rename(columns={'lat_x':'lat', 'long_x':'long','estimated_value_x':'est_value_manual', 'estimated_value_y':'est_value_rf'}, inplace=True)
    print('created comparisondf')
    #TODO: Find a way to get zipcode information; see what Yury is doing
    return comparisondf

def find_error_by_zipcode(df):
    ''' find_error_by_zipcode calculates the average error rates for both types of 
        estimations in each zipcode and adds these as new columns to df
        return: df with two added columns for error rates
    '''

    return

def create_combineddf(old_df):
    ''' create_combineddf compares the error rates of the two types of estimations in
        each zipcode, and creates a new dataframe with a new columns for the chosen 
        estimation values and for a boolean value is_manual which is 1 if the chosen
        estimation is manual, and 0 if it is random forest
        return: dataframe with columns
        ['prop_id', 'lat', 'long', 'est_value', 'is_manual', 'assess2021']
    '''

    return

def upload_combineddf(df):
    ''' upload_combineddf to heroku database as la_finalest_table
    '''
