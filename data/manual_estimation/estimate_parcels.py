
import os, sys
import pandas as pd
import statistics
import datetime
import collections

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'import_scripts')
sys.path.append(import_dir)
import import_to_heroku

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import get_data


class Estimator:
    def __init__(self, county, prop_id, rebase_year, roll_year, region, value):
        self.county = county
        self.prop_id = prop_id
        self.rebase_year = rebase_year
        self.roll_year = roll_year
        self.region = region
        self.value = value
        self.columns = [prop_id, rebase_year, roll_year, region, value]
        self.current_year = datetime.datetime.now().year

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
        if len(growth_map) == 0:
            return growth_map

        min_year = min(growth_map)
        prev_year = -1
        for year in range(min_year, self.current_year):
            if prev_year < 0:
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

        # iterate through each property and get growth
        ids = region_df[self.prop_id].unique()
        for id in ids:
            prop_df = region_df.loc[region_df[self.prop_id] == id]

            # only use re-assessed values to calculate growth
            prop_df = prop_df.loc[prop_df[self.rebase_year] == prop_df[self.roll_year]]
            prop_df = prop_df.sort_values(self.rebase_year) 
            prop_df = prop_df.reset_index()

            # if property has never been re-assessed, skip property
            if len(prop_df) < 2:
                continue

            # iterate through re-assessed years
            for index, row in prop_df.iterrows():
                curr_year = row[self.rebase_year]
                curr_value = row[self.value]
                if index == 0:
                    prev_year = curr_year
                    prev_value = curr_value
                    continue
                # value growth between re-assessment years
                diff_years = curr_year - prev_year
                compound_incr = pow(curr_value/prev_value, 1/diff_years)
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
        for i in range(int(start_year), int(end_year)):
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
        # compound growth from prev years to get cumulative growth
        growth_map = collections.OrderedDict(sorted(growth_map.items()))
        prev_year = -1
        for year, value in growth_map.items():  
            if prev_year < 0:
                # this is the first year. do nothing
                prev_year = year
                continue
            growth_map[year] = value * growth_map.get(year)
        return growth_map
    
    def most_recent_reassessments(self, df):
        """
        get the most recently re-assessed row for each property 
        (rows where rollyear = lastest rebase year)
        """
        df = df[[self.prop_id, self.rebase_year, self.value, self.roll_year]]

        # for each property, keep rows w latest reassessment year and choose oldest rollyear
        # to get last reassessed value
        idx_max_rebase_year = df.groupby(
            [self.prop_id])[self.rebase_year].transform(max) == df[self.rebase_year]
        df = df[idx_max_rebase_year]
        idx_min_roll_year = df.groupby([self.prop_id])[self.roll_year].transform(min) == df[self.roll_year]
        df = df[idx_min_roll_year]
        print(f"most recent assessments df is {df}")
        return df

    def estimate_current_parcel_values(self):
        """
        get current value estimation for each property
        this estimation is computed using the growth_by_region_map
        """
        self.get_df()
        growth_by_region = self.get_growth_by_region()
        region_dfs = []
        # for each region, estimate current property values
        for region, growth_map in growth_by_region.items():
            region_df = self.df.loc[self.df[self.region] == region]

            # keep only rows w most recently assessed property values
            region_df = self.most_recent_reassessments(region_df)
            print(f"region df is {region_df}")

            # use growth_by_region to get today's estimated parcel values
            current_value_est = {}
            for _, row in region_df.iterrows():
                prop_id = row[self.prop_id]
                last_assessed_year = row[self.rebase_year]
                print(f"last assessed year type is {type(last_assessed_year)} with val {last_assessed_year}")
                print(f"getting 2021 is {growth_map.get(2021)}")
                print(f"growth map is {growth_map}")

                growth_factor = growth_map.get(2021)/growth_map.get(int(last_assessed_year))

                current_value_est[prop_id] = growth_factor*row[self.value]
            
            region_df["current_value_estimation"] = current_value_est
            print(f"region df is {region_df}")
            region_dfs.append(region_df)
        
        output_df = pd.concat(region_dfs)
        print(f"final output is {output_df}")
        return output_df

def main():
    args = {'county': "la", 'prop_id': "ain", 'rebase_year': "landbaseyear", 'roll_year': "rollyear",
            'value': "totalvalue", 'region': "zipcode5"}
    estimator = Estimator(**args)
    tablename = "la_manual_est_table"
    df = estimator.estimate_current_parcel_values()

    # write table to heroku
    import_to_heroku.import_df(df, tablename)


if __name__ == "__main__":
    main()

