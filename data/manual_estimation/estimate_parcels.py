
import os, sys
import pandas as pd
import statistics
import datetime

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

    def average_counter(self, counter):
        for k in counter.keys():
            arr = counter.get(k)
            counter[k] = statistics.mean(arr)
        return counter

    def normalize_growth_map(self, growth_map):
        """
        inputs: growth map (map year to avg growth per year)

        1. we normalize the growth map by filling in missing years
        (no reported growth) with previous year's growth
        2. Fill in all years until today's year
        """
        today = datetime.datetime.now()
        min_year = min(growth_map)
        prev_year = -1
        for year in range(min_year, today.year):
            if prev_year == -1:
                prev_year = year
                continue

            if year not in growth_map.keys():
                growth_map[year] = growth_map.get(prev_year)
            prev_year = year
        return growth_map

    def get_growth_map(self, region_df):
        """
        input: region df has properties in a given region

        1. calculate the % increase in property value for each property in region_df
        2. look only at years when property was re-assessed and avg growth between those years
        3. add % growth to counter (maps year to array of % growths)
        4. make avg growth/year map and normalize

        output: normalized growth_map
        """
        counter = {}

        # get all properties in region and iterate through each property
        ids = region_df[self.prop_id].unique()
        for id in ids:
            prop_df = self.df.loc[self.df[self.prop_id] == id]

            # order from oldest to latest value update
            prop_df.sort_values(by=[self.rebase_year, self.row_year], inplace=True)
            rebase_years = prop_df[self.rebase_year].unique()

            # if property has never been re-assessed, skip property
            if len(rebase_years) <= 1:
                continue

            prev_year = prop_df[self.rebase_year].iloc[0]
            prev_value = prop_df[self.value].iloc[0]

            # calculate avg % growth between re-assessed property values
            for index in range(1, self.df.shape[0]):
                curr_year = self.df[self.rebase_year].iloc[index]
                curr_value = self.df[self.value].iloc[index]

                # if value was re-evaluated
                if curr_year > prev_year:
                    # calculate % increase between those years
                    diff_years = curr_year - prev_year
                    compound_incr = pow(curr_value/prev_value, 1/diff_years) - 1

                    counter = self.increase_counter(
                        counter, prev_year, curr_year, compound_incr)
                    
                    prev_year = curr_year
                    prev_value = curr_value

        # compute and return growth map for region
        growth_map = self.average_counter(counter)
        return self.normalize_growth_map(growth_map)


    def increase_counter(self, counter, start_year, end_year, perc):
        """
        add growth percentage to counter between start and end years
        """
        for i in range(start_year, end_year):
            if i in counter.keys():
                arr = counter.get(i)
                arr.append(perc)
            else:
                counter[i] = [perc]
        return counter

    def get_growth_by_region(self):
        """
        get growth map for each region

        output: growth_maps has key = region_id & value = growth_map
        (maps year to avg cumulative property value growth in that region)
        """
        regions = self.df[self.region].unique()
        growth_maps = {}

        for region in regions:
            region_df = self.df.loc[self.df[self.region] == region]
            growth_map = self.get_growth_map(region_df)
            growth_map = self.get_cumulative_growth(growth_map)
            growth_maps[region] = growth_map

        return growth_maps

    def get_cumulative_growth(self, growth_map): 
        """
        input: growth_map key = year & value = average property value growth in that year
        
        compute compound growth from first year in map
        """
        growth_map = {}
        # compound growth from prev years to get cumulative growth
        prev_year = -1
        for key, value in sorted(growth_map.iteritems()):
            if prev_year < 0:
                # this is the first year. do nothing
                continue
            growth_map[key] = value * (1 + growth_map.get(key))
        return growth_map
    
    def most_recent_reassessments(self, df):
        """
        get the most recently re-assessed row for each property 
        (rows where rollyear = lastest rebase year)
        """
        df = df[[self.prop_id, self.rebase_year, self.value, self.row_year]]

        # keep row with max rebase year for each prop_id
        df = df[df[self.row_year] == df.groupby(
            self.prop_id)[self.rebase_year].transform('max')]
        return df.reset_index()

    def estimate_current_parcel_values(self):
        """
        get current value estimation for each property
        this estimation is computed using the growth_by_region_map
        """
        growth_by_region = self.get_growth_by_region(self.df)

        # for each region, estimate current property values
        for region, growth_map in growth_by_region:
            region_df = self.df.loc[self.df[self.region] == region]

            # keep only rows w most recently assessed property values
            region_df = self.most_recent_reassessments(region_df)

            # use growth_by_region to get today's estimated parcel values
            current_value_est = {}
            for index, row in region_df.iterrows():
                prop_id = row[self.prop_id]
                last_assessed_year = row[self.rebase_year]
                growth_factor = growth_map.get()
            
            region_df["current_value_estimation"] = current_value_est

                

    
def main():
    args = {'county': "la", 'prop_id': "ain", 'rebase_year': "landbaseyear", 'row_year': "rollyear",
            'value': "totalvalue", 'region': "zipcode5"}
    estimator = Estimator(**args)
    estimator.get_df()
    estimator.estimate_parcels()


if __name__ == "__main__":
    main()

