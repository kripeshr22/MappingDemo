
import os, sys
import pandas as pd
import statistics

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data


class Estimator:
    def __init__(self, county, prop_id, rebase_year, row_year, region, value):
        self.county = county
        self.prop_id = prop_id
        self.rebase_year = rebase_year
        self.row_year = row_year
        self.region = region
        self.value = value
        self.columns = [prop_id, rebase_year, row_year, region, value]

    def get_df(self):
        """get df + format columns from input df: currently for la county only"""
        df = get_data.get_clean_df(self.county, self.columns)
        df = df.apply(pd.to_numeric)
        self.df = df
        return df

    def compute_average(self, counter):
        for k in counter.keys():
            arr = counter.get(k)
            counter[k] = statistics.mean(arr)
        return counter

    def get_increase(self):
        """get % increase in property values from prev year for each parcel
        and add perc_increase column"""
        counter = {}

        # for each property, compute % increase from prev landbaseyear
        # and add to counter
        ids = self.df[self.prop_id].unique()
        for id in ids:
            prop_df = self.df.loc[self.df[self.prop_id] == id]
            prop_df.sort_values(by=[self.rebase_year, self.row_year], inplace=True)
            print(prop_df)
            
            rebase_years = prop_df[self.rebase_year].unique()
            # if property has never been re-evaluated, skip property
            if len(rebase_years) <= 1:
                continue

            prev_year = prop_df[self.rebase_year].iloc[0]
            prev_value = prop_df[self.value].iloc[0]

            for index in range(1, self.df.shape[0]):
                curr_year = self.df[self.rebase_year].iloc[index]
                curr_value = self.df[self.value].iloc[index]

                # value was re-evaluated
                if curr_year > prev_year:
                    # calculate % increase between those years
                    diff_years = curr_year - prev_year
                    compound_incr = pow(curr_value/prev_value, 1/diff_years) - 1

                    counter = self.increase_counter(
                        counter, prev_year, curr_year, compound_incr)
                    
                    prev_year = curr_year
                    prev_value = curr_value
        return self.compute_average(counter)

    def increase_counter(self, counter, start_year, end_year, perc):
        for i in range(start_year, end_year):
            if i in counter.keys():
                arr = counter.get(i)
                arr.append(perc)
            else:
                counter[i] = [perc]
        return counter

    def get_growth_by_region(self):
        regions = self.df[self.region].unique()
        growth_maps = []

        for region in regions:
            df_split = self.df.loc[self.df[self.region] == region]
            growth_map = self.get_increase(df_split)
            growth_map = self.make_cumulative_growth(growth_map)
            growth_maps.append(growth_map)

        return zip(regions, growth_maps)

    def make_cumulative_growth(self, growth_map):
        cum_growth_map = {}
        # TODO: finish function

        return cum_growth_map

    
    def get_latest_values(self, df):
        df = df[[self.prop_id, self.rebase_year, self.value]]
        df = df.groupby(self.prop_id)
        df = df.max()
        df = df.reset_index()

    def estimate_parcels(self):
        growth_by_region = self.get_growth_by_region(self.df)

        # get splices of df by region
        for region, dict in growth_by_region:
            split_df = self.df.loc[self.df[self.region] == region]

            # get latest rebase year for each ain
            split_df = self.get_latest_values(split_df)

            # use growth_by_region to get current value for each parcel
            current_values = []
            for index, row in df.iterrows():
                

    
def main():
    args = {'county': "la", 'prop_id': "ain", 'rebase_year': "landbaseyear", 'row_year': "rollyear",
            'value': "totalvalue", 'region': "zipcode5"}
    estimator = Estimator(**args)
    estimator.get_df()
    estimator.estimate_parcels()


if __name__ == "__main__":
    main()

