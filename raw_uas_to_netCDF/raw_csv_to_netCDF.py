import pandas as pd
import xarray as xr
import numpy as np

# Read the CSV file into a pandas DataFrame
raw_uas = pd.read_csv('raw_uasdc.csv')

# Set 'obs' as the index of the DataFrame
raw_uas = raw_uas.set_index('obs')

# Create the xarray Dataset
ds = xr.Dataset.from_dataframe(raw_uas)

# Rename variables in xarray dataset to required variable names
rename_dict = {
    'lat' : 'latitude',
    'lon' : 'longitude',
    'altitude' : 'height',
    'air_temp': 'airTemperature',
    'dew_point': 'dewpointTemperature',
    'gpt' : 'nonCoordinateGeopotential',
    'gpt_height' : 'geopotentialHeight',
    'wind_speed' : 'windSpeed',
    'wind_dir' : 'windDirection',
    'mixing_ratio' : 'mixingRatio',
    'rel_hum' : 'relativeHumidity',
    'air_press' : 'pressure',

}

# Rename the variables within this xarray dataframe based on the rename dictionary above
ds = ds.rename(rename_dict)

# Convert Time to pandas datetime for translation
pd_time = pd.to_datetime(ds['time'])

# Convert Datetime to Seconds since EPOCH - netCDF files require FLOAT values for their time variable
ref_time = np.datetime64('1970-01-01T00:00:00')

ds = ds.drop('time')

# Convert time to seconds since the reference time
ds['time'] = (pd_time.values - ref_time) / np.timedelta64(1, 's')

# Convert Air Temperature from Celsius to Kelvin
ds['airTemperature'] = ds['airTemperature'] + 273.15

# Convert Dew Point Temperature from Celsius to Kelvin
ds['dewpointTemperature'] = ds['dewpointTemperature'] + 273.15

# Adding attributes to variables in the xarray dataset
ds['latitude'].attrs = {'units': 'degrees_north', 'long_name': 'Latitude'}
ds['longitude'].attrs = {'units': 'degrees_east', 'long_name': 'Longitude'}
ds['height'].attrs = {'units': 'meters', 'long_name': 'Altitude'}
ds['airTemperature'].attrs = {'units': 'Kelvin', 'long_name': 'Air Temperature'}
ds['dewpointTemperature'].attrs = {'units': 'Kelvin', 'long_name': 'Dew Point Temperature'}
ds['nonCoordinateGeopotential'].attrs = {'units': 'm^2 s^-2', 'long_name': 'Non-coordinate Geopotential'}
ds['geopotentialHeight'].attrs = {'units': 'meters', 'long_name': 'Geopotential Height'}
ds['windSpeed'].attrs = {'units': 'm/s', 'long_name': 'Wind Speed'}
ds['windDirection'].attrs = {'units': 'degrees', 'long_name': 'Wind Direction'}
ds['mixingRatio'].attrs = {'units': 'kg/kg', 'long_name': 'Mixing Ratio'}
ds['relativeHumidity'].attrs = {'units': '%', 'long_name': 'Relative Humidity'}
ds['pressure'].attrs = {'units': 'Pa', 'long_name': 'Atmospheric Pressure'}
ds['time'].attrs = {'units': 'seconds since 1970-01-01T00:00:00', 'long_name': 'Time'}

# Grab Initial timestamp of observations
timestamp_dt = pd.to_datetime(ds['time'].values[0], unit='s', origin='unix')

# Format datetime object to desired format (YYYYMMDDHHMMSSZ)
formatted_timestamp = timestamp_dt.strftime('%Y%m%d%H%M%S') + 'Z'

# Save to a NetCDF file
ds.to_netcdf(f'UASDC_operatorID_airframeID_processLevel_{formatted_timestamp}.nc')