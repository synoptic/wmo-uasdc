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
    'lat' : 'lat',
    'lon' : 'lon',
    'altitude' : 'altitude',
    'air_temp': 'air_temperature',
    'dew_point': 'dew_point_temperature',
    'gpt' : 'non_coordinate_geopotential',
    'gpt_height' : 'geopotential_height',
    'wind_speed' : 'wind_speed',
    'wind_dir' : 'wind_direction',
    'mixing_ratio' : 'humidity_mixing_ratio',
    'rel_hum' : 'relative_humidity',
    'air_press' : 'pressure',

}

# Rename the variables within this xarray dataframe based on the rename dictionary above
ds = ds.rename(rename_dict)

# Convert Time to pandas datetime for translation, store as separate object
pd_time = pd.to_datetime(ds['time'])

# Convert Datetime to Seconds since EPOCH - netCDF files require FLOAT values for their time variable
ref_time = np.datetime64('1970-01-01T00:00:00')

# we need to drop the time before we replace it (nuance of xarray)
ds = ds.drop_vars('time')

# Convert time to seconds since the reference time
ds['time'] = (pd_time.values - ref_time) / np.timedelta64(1, 's')

# Convert Air Temperature from Celsius to Kelvin
ds['air_temperature'] = ds['air_temperature'] + 273.15

# Convert Dew Point Temperature from Celsius to Kelvin
ds['dew_point_temperature'] = ds['dew_point_temperature'] + 273.15

# Adding attributes to variables in the xarray dataset
ds['time'].attrs = {'units': 'seconds since 1970-01-01T00:00:00', 'long_name': 'Time', 'fill_value': float('nan'), 'processing_level': ''}
ds['lat'].attrs = {'units': 'degrees_north', 'long_name': 'Latitude', 'fill_value': float('nan'), 'processing_level': ''}
ds['lon'].attrs = {'units': 'degrees_east', 'long_name': 'Longitude', 'fill_value': float('nan'), 'processing_level': ''}
ds['altitude'].attrs = {'units': 'meters', 'long_name': 'Altitude', 'fill_value': float('nan'), 'processing_level': ''}
ds['air_temperature'].attrs = {'units': 'Kelvin', 'long_name': 'Air Temperature', 'fill_value': float('nan'), 'processing_level': ''}
ds['dew_point_temperature'].attrs = {'units': 'Kelvin', 'long_name': 'Dew Point Temperature', 'fill_value': float('nan'), 'processing_level': ''}
ds['non_coordinate_geopotential'].attrs = {'units': 'm^2 s^-2', 'long_name': 'Non Coordinate Geopotential', 'fill_value': float('nan'), 'processing_level': ''}
ds['geopotential_height'].attrs = {'units': 'meters', 'long_name': 'Geopotential Height', 'fill_value': float('nan'), 'processing_level': ''}
ds['wind_speed'].attrs = {'units': 'm/s', 'long_name': 'Wind Speed', 'fill_value': float('nan'), 'processing_level': ''}
ds['wind_direction'].attrs = {'units': 'degrees', 'long_name': 'Wind Direction', 'fill_value': float('nan'), 'processing_level': ''}
ds['humidity_mixing_ratio'].attrs = {'units': 'kg/kg', 'long_name': 'Humidity Mixing Ratio', 'fill_value': float('nan'), 'processing_level': ''}
ds['relative_humidity'].attrs = {'units': '%', 'long_name': 'Relative Humidity', 'fill_value': float('nan'), 'processing_level': ''}
ds['pressure'].attrs = {'units': 'Pa', 'long_name': 'Atmospheric Pressure', 'fill_value': float('nan'), 'processing_level': ''}

# Grab Initial timestamp of observations
timestamp_dt = pd.to_datetime(ds['time'].values[0], unit='s', origin='unix')

# Format datetime object to desired format (YYYYMMDDHHMMSSZ)
formatted_timestamp = timestamp_dt.strftime('%Y%m%d%H%M%S') + 'Z'

# Save to a NetCDF file
ds.to_netcdf(f'UASDC_operatorID_airframeID_{formatted_timestamp}.nc')