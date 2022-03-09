from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys

current_dir = os.path.dirname(__file__)
import_dir = os.path.join(current_dir, '..', 'utils')
sys.path.append(import_dir)
import encode_zipcode as encode


def run_knn(df):
    # get encoded table
    X = df

    # Preliminary cleaning
    for col in X:
        # Removes any row where column value is ''
        X = X[X[col] != '']

        # Change data type to int and float
        X[col] = pd.to_numeric(X[col], downcast='integer')

    # Add land value per square foot to dataframe
    X['landvaluepersqft'] = X['landvalue']/X['sqftmain']

    # Clean data
    X = X[X['sqftmain'] != 0]
    X = X[X['landvaluepersqft'] < 1000]
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    # Set independent and dependent variables
    y = pd.DataFrame(X['landvaluepersqft'])
    X.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1)

    # Split data randomly - 30% used for test data; 70% used for training data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    # Create kNN Model
    knn = KNeighborsRegressor(n_neighbors=10)
    knn.fit(X_train, y_train)

    # Create predictions for test data
    y_pred = knn.predict(X_test)

    # Evaluate model
    plt.scatter(X_test['landbaseyear'], y_test, color="darkorange", label="data")
    plt.scatter(X_test['landbaseyear'], y_pred, color="navy", label="prediction")
    plt.legend(loc=1)
    plt.xlabel('Year')
    plt.ylabel('Land Value per sqft')
    plt.title("KNN Algorithm (k=10) on sample data")
    plt.show()

    fig = plt.figure(figsize=(6, 6))
    ax = plt.axes(projection='3d')

    ax.scatter3D(X_test['center_lat'], X_test['center_lon'],
                y_test, color="darkorange", label="data")
    ax.scatter3D(X_test['center_lat'], X_test['center_lon'],
                y_pred, color="navy", label="prediction")

    ax.legend(loc=1)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Land Value per sqft')
    plt.title("KNN Algorithm (k=10) on sample data")
    plt.show()

    # show error
    error = sqrt(mean_squared_error(y_test, y_pred))
    print(f"mean squared error is {error}")

    # Create a dataframe that contains all columns, but only rows where landbaseyear is 2021
    X_assess = X.copy()
    X_assess = X_assess[X_assess['landbaseyear'] == 2021]

    # Set dependent and independent varaibles for the properties that were assessed in 2021 (y_assess_pred),
    y_assess = pd.DataFrame(X_assess['landvaluepersqft'])
    X_assess.drop(['landvalue', 'sqftmain', 'landvaluepersqft'], axis=1)

    # Make predictions for the properties that were assessed in 2021
    y_assess_pred = knn.predict(X_assess)

    # Compare predictions to actual values
    print("For properties assessed in 2021")
    print("Mean predicted LV/sqft: ", y_assess_pred.mean())
    print("Mean actual LV/sqft: ", y_assess['landvaluepersqft'].mean())
    print("St. Dev of predicted LV/sqft: ", y_assess_pred.std())
    print("St. Dev of actual LV/sqft: ", y_assess['landvaluepersqft'].std())
    print("Mean error: ", sqrt(mean_squared_error(y_assess, y_assess_pred)))

    # Create a copy of X, but with all landbaseyear values replaced with 2021
    X_current = X.copy()
    X_current["landbaseyear"] = 2021

    # Predict land value for each property if it were assessed in 2021 based on latitude and longitude
    y_current = knn.predict(X_current)

    # Plot the predictions for land value per sqft if properties were assessed in 2021
    fig = plt.figure(figsize=(6, 6))
    ax = plt.axes(projection='3d')
    ax.scatter3D(X_current['center_lat'],
                X_current['center_lon'], y_current, color="navy")
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Land Value per sqft')

    plt.title("Predictions of current land value per square foot if properties were assessed in 2021")
    plt.show()


def main():
    select_cols = ['landbaseyear','center_lat', 'center_lon', 'yearbuilt', 'effectiveyearbuilt',
        'landvalue','sqftmain', 'zipcode5']
    hash_df = encode.main("hash", select_cols)
                           
    run_knn(hash_df)

if __name__ == "__main__":
    main()
