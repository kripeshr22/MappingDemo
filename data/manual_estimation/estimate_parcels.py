
import os, sys
import pandas as pd

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data

def format_df(df):
    """clean columns from input df: currently for la county only"""
    df = df.apply(pd.to_numeric)
    return df

def get_increase(df, prop_id, rebase_year, row_year, value):
    """get % increase in property values from prev year for each parcel
    and add perc_increase column"""
    counter = {}

    # for each property, compute % increase from prev landbaseyear
    count = 0
    ids = df[prop_id].unique()
    for id in ids:
        prop_df = df.loc[df[prop_id] == id]
        prop_df.sort_values(by=[rebase_year, row_year], inplace=True)
        print(prop_df)
        
        rebase_years = prop_df[rebase_year].unique()
        if len(rebase_years) < 2:
            continue

        prev_year = prop_df[rebase_year].iloc[0]
        prev_value = prop_df[value].iloc[0]

        for index in range(1, df.shape[0]):
            curr_year = df[rebase_year].iloc[index]
            curr_value = df[value].iloc[index]

            # value was re-evaluated
            if curr_year > prev_year:
                # calculate % increase between those years
                diff_years = curr_year - prev_year
                compound_incr = pow(curr_value/prev_value, 1/diff_years) - 1

                counter = increase_counter(
                    counter, prev_year, curr_year, compound_incr)
                
                prev_year = curr_year
                prev_value = curr_value
            
        count += 1
        if count == 1:
            print(counter)
            break


def increase_counter(counter, start_year, end_year, perc):
    # start_year = int(start_year)
    # end_year = int(end_year)
    for i in range(start_year, end_year):
        if i in counter.keys():
            arr = counter.get(i)
            arr.append(perc)
        else:
            counter[i] = [perc]
    return counter

def estimate_parcels():
    cols = ["zipcode5", "rollyear", "landbaseyear", "totalvalue", "ain"]
    df = get_data.get_clean_df("la", cols)
    df = format_df(df)

    zipcodes = df['zipcode5'].unique()
    print(zipcodes[0:10])
    for zipcode in zipcodes:
        df_split = df.loc[df["zipcode5"] == zipcode]
        df_split = get_increase(df_split, 'ain', 'landbaseyear', 'rollyear', 'totalvalue')
        break




    # print(df.head())

if __name__ == "__main__":
    estimate_parcels()

