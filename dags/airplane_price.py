#airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

#import python libaries for data preprocessing
import pandas as pd
import numpy as np
from scipy.stats import yeojohnson
import sklearn.preprocessing as preproc
from sklearn.preprocessing import StandardScaler
import os

#import python libaries for training

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
#import xgboost 
#from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

def data_preprocessing(ti, path="/opt/airflow/data/raw_data/Clean_Dataset.csv"):
    
    """
    This script performs data preprocessing tasks on a flight dataset. It includes the following steps:

    1. Read the dataset from a CSV file.
    2. Convert ordinal categorical variables to numerical values.
    3. Perform one-hot encoding for selected categorical variables.
    4. Apply the Yeo-Johnson transformation to ensure normal distribution for continuous variables.
    5. Standardize specific columns using StandardScaler.
    6. Remove outliers separately for Economy and Business class based on price.
    7. Save cleaned datasets for Economy and Business class in CSV files.
    8. Create a context directory containing file paths for the saved data.
    9. Push the context directory to the next stage in the workflow using XCom.

    Note: This script assumes specific column names and file paths and is part of a larger data processing pipeline.
    """

    
    df = pd.read_csv(path)
    print(df)
    
    #ordinal numerical conversion
    stops_dict = {'zero' : 0, 'one' : 1, 'two_or_more' : 2}
    df['stops'] = df['stops'].replace(stops_dict).astype(int)
    
    class_dict = {'Economy' : 0, 'Business' : 1}
    df['class'] = df['class'].replace(class_dict).astype(int)

    #onehot encoding using dummy variable
    dummies_variable = ['airline', 'source_city', 'departure_time', 'arrival_time', 'destination_city']
    dummies = pd.get_dummies(df[dummies_variable], drop_first= True).astype(int)

    df = pd.concat([df, dummies], axis = 1) #coloumnwise

    #drop the columns which have already encoded
    df = df.drop(['Unnamed: 0', 'airline', 'flight', 'source_city', 'departure_time', 'arrival_time', 'destination_city'], axis = 1)
    
    #print dataset
    print(df.head())
    
    #apply yeojohson for contineous variable for normal distribution
    col = "duration"
    y_value, _ = yeojohnson(df[col])
    df[col] = y_value
    
    #standardization of dataset
    cols = ['duration', 'days_left']
    df[cols] = StandardScaler().fit_transform(df[cols])
    
    #remove outliers 
    #for economy class
    price = df[df['class']==0].price
    lower_limit = price.mean() - 3*price.std()
    upper_limit = price.mean() + 3*price.std()

    print("----ECONOMY CLASS-----")
    print("lower_limit: {:.3f}".format(lower_limit))
    print("upper_limit: {:.3f}".format(upper_limit))

    class_eco = df[(df['class']==0) &
                        (df['price'] >= lower_limit) &
                        (df['price'] <= upper_limit)].index

    #for business class
    price = df[df['class']==1].price
    lower_limit = price.mean() - 3*price.std()
    upper_limit = price.mean() + 3*price.std()

    print("----BUSINESS CLASS-----")
    print("lower_limit: {:.3f}".format(lower_limit))
    print("upper_limit: {:.3f}".format(upper_limit))

    class_bsn = df[(df['class']==1) &
                        (df['price'] >= lower_limit) &
                        (df['price'] <= upper_limit)].index

    
    
    print("minimum price over whole dataset: {:.4f}".format(df['price'].min()))
    print("maximum price over whole dataset: {:.4f}".format(df['price'].max()))

    #total no of outlier dropped
    count_class_eco = len(class_eco)
    count_class_bsn = len(class_bsn)
    count_df = len(df['price'])

    num_of_outlier_data = count_df - count_class_bsn - count_class_eco
    print("total number of outlier data: {}".format(num_of_outlier_data))
    
    #it will create directory if requires for storing the data
    try:
        os.makedirs("/opt/airflow/data/feature/")
    except:
        pass
    #save the csv files for economy and business class
    df.iloc[class_eco].to_csv("/opt/airflow/data/feature/eco_features_details.csv", index=False)
    df.iloc[class_bsn].to_csv("/opt/airflow/data/feature/bsn_features_details.csv", index=False)
    
    context_directory = {
        "business" : "/opt/airflow/data/feature/bsn_features_details.csv",
        "economy" : "/opt/airflow/data/feature/eco_features_details.csv"
    }
    
    #pushing data to next stage
    ti.xcom_push(key = "data_preparation_context", value = context_directory)
    
    return None
#define function for business class

def business_class_training(ti):
    
    """
    This function is responsible for training a machine learning model for the Business class pricing prediction using the preprocessed data. It performs the following steps:

    1. Pulls the preprocessed data of the Business class from a context directory via XCom.
    2. Reads the features and target variable from the data.
    3. Splits the data into training and testing sets.
    4. Initializes a K-Nearest Neighbors (KNN) regression model.
    5. Fits the KNN model to the training data.
    6. Makes predictions on the testing data.
    7. Computes the Mean Absolute Error (MAE) between the predicted and actual prices.
    8. Prints the selected model and the calculated MAE for Business class pricing.

    Parameters:
        - ti: The TaskInstance object used for interacting with the Airflow environment.

    Returns:
        - None

    Note: This function assumes specific data preprocessing has been performed and is part of a larger workflow.
    """

    #pull the data of business
    directory_dict = ti.xcom_pull(key = "data_preparation_context")
    file_name = directory_dict['business']
    feature = pd.read_csv(file_name)
    target = feature.pop("price")
    #traintest split
    X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size =0.20, random_state=42, shuffle=True)
    
    model = KNeighborsRegressor()
    print("selected model for business Class: ", model)
    trained_model = model.fit(X_train, y_train)
    y_pred = trained_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"business class mean_absolute_error: {mae}")

    return None

#define function for economy class

def economy_class_training(ti):
    
    """
    This function is responsible for training a machine learning model for the Economy class pricing prediction using the preprocessed data. It performs the following steps:

    1. Pulls the preprocessed data of the Economy class from a context directory via XCom.
    2. Reads the features and target variable from the data.
    3. Splits the data into training and testing sets.
    4. Initializes a K-Nearest Neighbors (KNN) regression model.
    5. Fits the KNN model to the training data.
    6. Makes predictions on the testing data.
    7. Computes the Mean Absolute Error (MAE) between the predicted and actual prices.
    8. Prints the selected model and the calculated MAE for Economy class pricing.

    Parameters:
        - ti: The TaskInstance object used for interacting with the Airflow environment.

    Returns:
        - None

    Note: This function assumes specific data preprocessing has been performed and is part of a larger workflow.
    """

    #pull the data of economy
    directory_dict = ti.xcom_pull(key = "data_preparation_context")
    file_name = directory_dict['economy']
    feature = pd.read_csv(file_name)
    target = feature.pop("price")
    #traintest split
    X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size =0.20, random_state=42, shuffle=True)
    
    model = KNeighborsRegressor()
    print("selected model for economy Class: ", model)
    trained_model = model.fit(X_train, y_train)
    y_pred = trained_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"economy class mean_absolute_error: {mae}")
    
    return None

#prepare dag
airplane_dag = DAG(
    "Airline_ticket_price_prediction_DAG",
    # schedule_interval="@daily",
    schedule_interval=None,
    start_date=datetime(2023, 9, 2),
)

#assign tasks
with airplane_dag:
    
    #preprocessing
    data_preparation_task = PythonOperator(
        task_id="data_preparation", python_callable=data_preprocessing, provide_context=True,
    )
    
    #business class
    bsn_training_task = PythonOperator(
        task_id="bsn_training_task", python_callable=business_class_training, provide_context=True
    )
    
    #economy class
    eco_training_task = PythonOperator(
        task_id="eco_training_task", python_callable=economy_class_training, provide_context=True
    )

   

    data_preparation_task >> [bsn_training_task, eco_training_task]