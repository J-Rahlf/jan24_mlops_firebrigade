# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pyproj import Proj, Transformer
from geopy.distance import geodesic
from datetime import datetime

print('jr_preprocessing startet')
# Read the CSV file
# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
print('X', script_dir)

# Navigate to the project directory (two parent directories up from the script directory)
project_dir = os.path.dirname(os.path.dirname(script_dir))
print('X', project_dir)

# Construct the file path relative to the current working directory
file_path = os.path.join(project_dir, "data", "raw", "df_i.csv")
print('X', file_path)


# Read the CSV file
df_i = pd.read_csv(file_path)

# List of desired columns
columns_to_keep = ['IncidentNumber', 'DateOfCall', 'CalYear', 'HourOfCall',
                   'IncGeo_BoroughName', 'Easting_m', 'Northing_m',
                   'Easting_rounded', 'Northing_rounded', 'Latitude',
                   'Longitude', 'FirstPumpArriving_AttendanceTime',
                   'FirstPumpArriving_DeployedFromStation']

# Select the desired columns
df_i2 = df_i[columns_to_keep].copy()  # Create a copy of the DataFrame

# Rename columns
df_i2.rename(columns={'FirstPumpArriving_AttendanceTime': 'AttendanceTime',
                      'FirstPumpArriving_DeployedFromStation': 'DeployedFromStation'}, inplace=True)


# Convert geodata and add columns

# Definition of the Ordnance Survey Grid Reference Project (OSGB)
osgb_proj = Transformer.from_crs("EPSG:27700", "EPSG:4326")   # EPSG code 27700 corresponds to OSGB (Ordnance Survey Grid)

# Define a function to convert UTM coordinates to WGS84
def utm_to_wgs84(easting, northing):
    lat, lon = osgb_proj.transform(easting, northing)
    return lat, lon

# Define a function to apply UTM to WGS84 conversion to each row and add the results as new columns
def utm_to_wgs84_wrapper(row):
    lat_cal, long_cal = utm_to_wgs84(row['Easting_m'], row['Northing_m'])
    lat_cal_r, long_cal_r = utm_to_wgs84(row['Easting_rounded'], row['Northing_rounded'])
    return pd.Series({'lat_cal': lat_cal, 'long_cal': long_cal, 'lat_cal_r': lat_cal_r, 'long_cal_r': long_cal_r})

# Apply the conversion function to each row and add the results as new columns
with pd.option_context('mode.chained_assignment', None):  # Suppress SettingWithCopyWarning
    df_i2[['lat_cal', 'long_cal', 'lat_cal_r', 'long_cal_r']] = df_i2.apply(utm_to_wgs84_wrapper, axis=1)

# Construct the file path relative to the current working directory
file_path = os.path.join(project_dir, 'data/external/stations_boroughs_1.csv')
df_stations_boroughs = pd.read_csv(file_path)

# Merge based on the 'FirstPumpArriving_DeployedFromStation' column
df_mi2 = pd.merge(
    df_i2,  # Left DataFrame
    df_stations_boroughs[['stat', 'lat', 'long', 'bor_sqkm', 'pop_per_stat', 'distance_stat']],
    left_on='DeployedFromStation',  # Column to merge on in df_i2
    right_on='stat',  # Column to merge on in stations_boroughs
    how='left'  # Type of merge (in this case, left)
)


# Calculate and add 'distance' btween incident and firestation

def calculate_distance(row):
    # Check if latitude values are within the expected range
    if pd.notna(row['Latitude']) and pd.notna(row['lat']):
        valid_latitudes = all(49 <= lat <= 53 for lat in [row['Latitude'], row['lat']])
        if not valid_latitudes:
            return None

    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']) and pd.notna(row['lat']) and pd.notna(row['long']):
        # If both sets of coordinates are present, calculate the distance
        coord1 = (row['Latitude'], row['Longitude'])
        coord2 = (row['lat'], row['long'])
        return geodesic(coord1, coord2).meters
    elif pd.notna(row['lat_cal_r']) and pd.notna(row['long_cal_r']) and pd.notna(row['lat']) and pd.notna(row['long']):
        # If 'Latitude' and 'Longitude' are not present, use 'lat_cal_r' and 'long_cal_r'
        coord1 = (row['lat_cal_r'], row['long_cal_r'])
        coord2 = (row['lat'], row['long'])
        return geodesic(coord1, coord2).meters
    else:
        return 0  # Replace NaN with 0 for distance

# Calculate and add 'distance' column
df_mi2['distance'] = df_mi2.apply(calculate_distance, axis=1)


# Delete 'Easting_m',  ' Northing_m', 'Latitude', 'Longitude'

# List of columns to remove
columns_to_remove = ['Easting_m', 'Northing_m', 'Latitude', 'Longitude']

# Remove the columns from the DataFrame
df_mi2 = df_mi2.drop(columns=columns_to_remove)

# Remove all rows with NaN values
df_mi2 = df_mi2.dropna()

# Convert 'AttendanceTime' to minutes and then classify into time intervals
df_mi2['AttendanceTimeClasses3'] = pd.cut(df_mi2['AttendanceTime'] / 60, bins=[0, 3, 6, 9, 12, 15, float('inf')], labels=['0-3min', '3-6min', '6-9min', '9-12min', '12-15min', '> 15min'])

# Save processed file in ../data/processed/

# File path to save the processed CSV file
output_file_path = os.path.join(project_dir, 'data/processed/df_mi5_5.csv')

# Save the DataFrame as a CSV file
df_mi2.to_csv(output_file_path, index=False)

#Timestamp as envirement variable
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
current_datetime = current_datetime[:-4]  
os.environ['CURRENT_DATETIME'] = current_datetime

print(os.environ['CURRENT_DATETIME'])

print("Current datetime from program:", current_datetime)
