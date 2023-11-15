import pandas as pd
import xarray as xr

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
    'wind_dir' : 'windDir',
    'mixing_ratio' : 'mixingRatio',
    'rel_hum' : 'relativeHumidity',
    'air_press' : 'pressure',

}

# Rename the variables within this xarray dataframe based on the rename dictionary above
ds = ds.rename(rename_dict)

# Convert Air Temperature from Celsius to Kelvin
ds['airTemperature'] = ds['airTemperature'] + 273.15

# Convert Dew Point Temperature from Celsius to Kelvin
ds['dewpointTemperature'] = ds['dewpointTemperature'] + 273.15

# Grab Initial timestamp of observations
timestamp_dt = pd.to_datetime(ds['time'].values[0]).to_pydatetime()

# Format datetime object to desired format (YYYYMMDDHHMMSSZ)
formatted_timestamp = timestamp_dt.strftime('%Y%m%d%H%M%S') + 'Z'

# Save to a NetCDF file
ds.to_netcdf(f'UASDC_operatorID_airframeID_processLevel_{formatted_timestamp}.nc')