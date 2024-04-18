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
    'rel_hum' : 'relative_humidity',
    'air_press' : 'air_pressure',

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

# Adding a REQUIRED Variable to the Dataset 
ds['humidity_mixing_ratio'] = np.nan

# Adding attributes to variables in the xarray dataset
ds['time'].attrs = {'units': 'seconds since 1970-01-01T00:00:00', 'long_name': 'Time', '_FillValue': float('nan'), 'processing_level': ''}
ds['lat'].attrs = {'units': 'degrees_north', 'long_name': 'Latitude', '_FillValue': float('nan'), 'processing_level': ''}
ds['lon'].attrs = {'units': 'degrees_east', 'long_name': 'Longitude', '_FillValue': float('nan'), 'processing_level': ''}
ds['altitude'].attrs = {'units': 'meters_above_sea_level', 'long_name': 'Altitude', '_FillValue': float('nan'), 'processing_level': ''}
ds['air_temperature'].attrs = {'units': 'Kelvin', 'long_name': 'Air Temperature', '_FillValue': float('nan'), 'processing_level': ''}
ds['dew_point_temperature'].attrs = {'units': 'Kelvin', 'long_name': 'Dew Point Temperature', '_FillValue': float('nan'), 'processing_level': ''}
ds['non_coordinate_geopotential'].attrs = {'units': 'm^2 s^-2', 'long_name': 'Non Coordinate Geopotential', '_FillValue': float('nan'), 'processing_level': ''}
ds['geopotential_height'].attrs = {'units': 'meters', 'long_name': 'Geopotential Height', '_FillValue': float('nan'), 'processing_level': ''}
ds['wind_speed'].attrs = {'units': 'm/s', 'long_name': 'Wind Speed', '_FillValue': float('nan'), 'processing_level': ''}
ds['wind_direction'].attrs = {'units': 'degrees', 'long_name': 'Wind Direction', '_FillValue': float('nan'), 'processing_level': ''}
ds['humidity_mixing_ratio'].attrs = {'units': 'kg/kg', 'long_name': 'Humidity Mixing Ratio', '_FillValue': float('nan'), 'processing_level': ''}
ds['relative_humidity'].attrs = {'units': '%', 'long_name': 'Relative Humidity', '_FillValue': float('nan'), 'processing_level': ''}
ds['air_pressure'].attrs = {'units': 'Pa', 'long_name': 'Atmospheric Pressure', '_FillValue': float('nan'), 'processing_level': ''}

# Add Global Attributes synonymous across all UASDC providers
ds.attrs['Conventions'] = "CF-1.8, WMO-CF-1.0"
ds.attrs['wmo__cf_profile'] = "FM 303-2024"
ds.attrs['featureType'] = "trajectory"

# Add Global Attributes unique to Provider
ds.attrs['platform_name'] = "GS_weatherhive"
ds.attrs['flight_id'] = "JBCC_1500m_VP"
ds.attrs['site_terrain_elevation_height'] = "3200m"
ds.attrs['processing_level'] = "raw"

# Grab Initial timestamp of observations
timestamp_dt = pd.to_datetime(ds['time'].values[0], unit='s', origin='unix')

# Format datetime object to desired format (YYYYMMDDHHMMSSZ)
formatted_timestamp = timestamp_dt.strftime('%Y%m%d%H%M%S') + 'Z'

# Save to a NetCDF file
ds.to_netcdf(f'UASDC_operatorID_airframeID_{formatted_timestamp}.nc')
