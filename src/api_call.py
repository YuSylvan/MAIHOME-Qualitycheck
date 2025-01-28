import requests
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import os
import sys
import pandas as pd
import json
from tqdm import tqdm
from requests.exceptions import HTTPError, Timeout, RequestException

#Set the environment variable "CALCULUS_API_KEY ' to your token and restart the device
token = os.getenv("CALCULUS_API_KEY", "***")
headers = {
    "CalculusApiKey" : token
}

base_url = 'https://api.calculus.group/v3'

def query_endpoint(endpoint, header, assetid=None, start_time=None, end_time=None, dry_run=True,timeout_seconds = 100):
    """
    Queries the specified API endpoint.

    Parameters:
        base_url (str): The base URL of the API.
        endpoint (str): The specific endpoint to query.
        id (int, optional): The identifier to include in the endpoint URL.
        start_time (datetime, optional): The start time for time-based queries. 
            Should be a timezone-aware datetime object.
        end_time (datetime, optional): The end time for time-based queries. 
            Should be a timezone-aware datetime object.
        dry_run (bool, optional): If True, only prints the URL without making the request. 
            Default is False.

    Returns:
        dict or None: The JSON response from the API if the request is successful,
            None if there is an error or if dry_run is True.
    """
    url = f"{base_url}/assets"
    
    if assetid is not None:
        url += f"/{assetid}"
    
    url += f"/{endpoint}"
    
    if start_time is not None and end_time is not None:
        start_unix = datetime_to_unix(start_time)
        end_unix = datetime_to_unix(end_time)
        url += f"?unixTimestampStart={start_unix}&unixTimestampEnd={end_unix}"
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()  # Raises HTTPError if response status code is not 2xx
        return response.json()
    except Timeout:
        # print("The request timed out")
        return 'Timeout'
    except HTTPError as e:
        # print(f"HTTP error occurred: {e}")
        return 'HTTP Error'
    except RequestException as e:
        # print(f"An error occurred while making the request: {e}")
        return 'Other API Error'



def datetime_to_unix(dt):
    """Converts a datetime object to Unix timestamp."""
    # Ensure the datetime object has time zone information
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        raise ValueError("Datetime object must have time zone information")

    # Convert datetime to UTC timezone
    dt_utc = dt.astimezone(ZoneInfo("UTC"))

    # Calculate Unix timestamp
    unix_timestamp = (dt_utc - datetime(1970, 1, 1, tzinfo=ZoneInfo("UTC"))).total_seconds()
    return int(unix_timestamp)

def extract_reading_data(data, pid):
    reading_data = []
    for source in data['dataSources']:
        sensor_name = source['name']
        for series in source['dataSeries']:
            key_parts = series['key'].split('|')
            sensor_key = key_parts[1].split('#')[0]  # Extracting sensor key (e.g., 'battery', 'co2', etc.)
            for entry in series['value']:
                timestamp = entry['key']
                value = entry['value']
                reading_data.append({'SensorID': pid, 'SensorType': sensor_name, 'Timestamp': timestamp, sensor_key: value})
    return reading_data

def load_assets_from_json(filepath):
    """
    Load asset data from a specified JSON file.
    
    This function reads a JSON file from the given filepath and parses its content into a Python data structure.
    
    Parameters:
        filepath (str): The path to the JSON file to be read.
        
    Returns:
        A list
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)



def getdf(assetid,response):
    
    reading_data = extract_reading_data(response, assetid)
    df = pd.DataFrame(reading_data)
    df=df.groupby('Timestamp').agg('first').reset_index()
    columns_to_check = df.columns.difference(['Timestamp', 'SensorID', 'SensorType'])
    df = df.dropna(subset=columns_to_check, how='all')

    return df

def check_thresholds(df, thresholds):
    """
    Check if the DataFrame values meet the threshold criteria.

    Parameters:
        df (DataFrame): The data to check.
        thresholds (dict): A dictionary of column thresholds to check against.

    Returns:
        str: "TRUE" if all checks pass, otherwise a string listing the failed column names.
    """
    failed_columns = []
    for column, limits in thresholds.items():
        if column in df.columns:
            min_value = limits.get('min')
            max_value = limits.get('max')
            
            # Check minimum threshold if defined
            if min_value is not None and (df[column] < min_value).any():
                failed_columns.append(column)
                continue
            
            # Check maximum threshold if defined
            if max_value is not None and (df[column] > max_value).any():
                failed_columns.append(column)
                continue

            # # Check for null values
            # if df[column].isnull().any():
            #     failed_columns.append(column)
            #     continue

    return "TRUE" if not failed_columns else ", ".join(failed_columns)

def check_import_data(assets, db_manager = None, start_time=datetime.now(ZoneInfo("UTC")) - timedelta(hours=12), end_time=datetime.now(ZoneInfo("UTC"))):

    results = []
    thresholds_MAI = {
        'active_power': {'min': 0, 'max': 1000}, 
        'battery': {'min': 0, 'max': 100}, 
        'co2': {'min': 0, 'max': 5000},    
        'current': {'min': 0, 'max': 1000},    
        'humidity': {'min': 0, 'max': 100},     
        'temperature': {'min': -20, 'max': 50},  
        'setTemperature': {'min': -20, 'max': 50}, 
        'temperature.current': {'min': -20, 'max': 50},  
        'temperature.set': {'min': -20, 'max': 50},    
        'pressure': {'min': 900, 'max': 1100},  
        'tvoc' : {'min': 0, 'max': 1000},
    }


    for asset in tqdm(assets, desc="Processing assets", unit="asset"):
        asset_id = asset['id']
        asset_type = asset['type']
        asset_key = asset['key']
        asset_name = asset['name']
        

        # Query the API endpoint for data aggregates using the provided asset ID and time range
        response = query_endpoint('aggregateseries', headers, assetid=asset_id, start_time=start_time, end_time=end_time, dry_run=False)
        
        # Determine data availability from the API response
        if type(response) == dict:
            has_data = True
        else:
            has_data = response
   
        # Initialize the flag for checking NaN values outside specific columns
        check_nan = "No Data"
        threshold_check = "No Data"

        # Check column consistency
        # columns_match = False
        if has_data == True:
            reading_data = extract_reading_data(response, asset_id)
            df = pd.DataFrame(reading_data)
            df = df.groupby('Timestamp').agg('first').reset_index()
            data_columns = [col for col in df.columns if col not in ['Timestamp', 'SensorID', 'SensorType']]
            if not df[data_columns].dropna(how='all', axis=1).empty:
                check_nan = True
            else:
                check_nan = False

        data_availability = has_data == True and check_nan == True
    

        # If data is available, check data check_thresholds and import it into db
        if data_availability:
            datadf = getdf(asset_id,response)
            threshold_check = check_thresholds(datadf, thresholds_MAI)
            if db_manager != None:
                datadf = getdf(asset_id,response)
                db_manager.insert_readings(datadf)
                
     
        results.append({
            'Asset ID': asset_id,
            'Asset Type': asset_type,
            'Asset key': asset_key,
            'Asset name': asset_name,
            'Has Data (API)': has_data,
            'Check NaN': check_nan,
            'data_availability': data_availability,
            'threshold_check': threshold_check

        })
    
    results = pd.DataFrame(results)

    data_available_count = results['data_availability'].sum()
    threshold_error_count = data_available_count- (results['threshold_check'] == "TRUE").sum()

    start_time_str = start_time.strftime('%Y-%m-%d_%H')
    end_time_str = end_time.strftime('%Y-%m-%d_%H')
    filename = f'results from {start_time_str} to {end_time_str}.csv'
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Dataresult'))

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = os.path.join(save_path, filename)
    results.to_csv(file_path, index=False)

    print(f"Total assets processed: {len(assets)}. Assets with available data: {data_available_count}, among them assets with threshold errors: {threshold_error_count}.")
    return results