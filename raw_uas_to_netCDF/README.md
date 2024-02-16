
# UAS netCDF Files
It's imperative that each provider contains netCDF files with correct structure, naming conventions, and units. An example file for the proposed format [can be found here](../nc2bufr/UASDC_operatorID_airframeID_20230327025804Z.nc). **Please ensure that your UASDC netCDF files have the correct filename structure, variable names, and units.**

## Filename Structure

**UASDC_operatorID_airframeID_YYYYMMDDHHMMSSZ.nc**

| Component        | Description                                                                                     |
|------------------|-------------------------------------------------------------------------------------------------|
| `operatorID`     | 3 digit unique Operator ID assigned to each UAS data provider.                                                   |
| `airframeID`     | 5 digit provider assigned Airfame ID                                       |
| `YYYY`           | 4 digit Year at start of flight                                                                                |
| `MM`             | 2 digit Month at start of flight                                                                                  |
| `DD`             | 2 digit Day at start of flight                                                                                    |
| `HH`             | 2 digit Hour at start of flight                                                                                   |
| `SS`             | 2 digit Second at start of flight                                                                                 |
| `Z`              | Zulu time. All data should be stored in UTC, following the ISO8601 open data standard.         |

Example Filename:

**UASDC_007_12345_202402152200Z.nc**

Please note that **the timestamp used in the filename represents the start time of observations**. If you follow the [the raw csv to netcdf file example](raw_csv_to_netCDF.py), the script will grab timestamp 0, or, in Python, the initial timestamp of observations. 

## Variable Names and Units

Below are the variables that will be converted to BUFR. Please ensure the variable names and units match the table below. If you do not have all of these variables in your raw data, that is OK, the program will still run without them. Note that these variable names are consistent with BUFR official variable names.

| Long Name                                          | Short Name                                          | Required Variable Name                               | Required Units        |
|----------------------------------------------------|----------------------------------------------------|------------------------------------------------------|-----------------------|
| Time                                               | Time                                               | `time`                                               | Seconds since EPOCH (1970-01-01T00:00:00) | 
| Latitude                                           | Latitude                                           | `lat`                                           | degrees (-90 to 90)   |
| Longitude                                          | Longitude                                          | `lon`                                          | degrees (-180 to 180) |
| Altitude (height)                                  | Altitude                              | `altitude`                                             | Meters                |
| Air Temperature                                    | Air Temperature                                    | `air_temperature`                                     | Kelvin                |
| Air Dewpoint Temperature                               | Dewpoint Temperature                               | `dew_point_temperature`                                | Kelvin                |
| Wind Direction                                     | Wind Direction                                     | `wind_direction`                                      | degrees               |
| Wind Speed                                         | Wind Speed                                         | `wind_speed`                                          | m/s                   |
| Relative Humidity                                  | Relative Humidity                                  | `relative_humidity`                                   | %                     |
| Humidity Mixing Ratio                              | Mixing Ratio                                       | `humidity_mixing_ratio`                                        | kg/kg                 |
| Turbulent Kinetic Energy                           | Turbulent Kinetic Energy                           | `turbulent_kinetic_energy`                             | m2 s-2                |
| Mean Turbulence Intensity Eddy Dissipation Rate    | Eddy Dissipation Rate                              | `eddy_dissipation_rate`                               | m2/3 s-1              |
| Air Pressure                                       | Air Pressure                                       | `air_pressure`                                           | Pascals               |
| Geopotential                                       | Geopotential                                       | `non_coordinate_geopotential`                          | m2 s-2                |
| Geopotential Height                                | Geopotential Height                                | `geopotential_height`                                 | geopotential meters   |


Please refer to the example netCDF file, [UASDC_operatorID_airframeID_20230327025804Z.nc](../nc2bufr/UASDC_operatorID_airframeID_20230327025804Z.nc), for more information if needed. 

# Raw UASDC CSV to netCDF example

An example using `pandas` and `xarray` to convert raw UAS csv data [can be found here](raw_csv_to_netCDF.py). The raw csv file being used for this script [can be found here](raw_uasdc.csv)

## Environment setup

There are 3 python packages required for the raw UASDC CSV to netCDF example. These packages are `xarray`, `pandas`, and `numpy`. They can be installed via `pip` or `conda`. Please also note that **we need to store time as seconds since EPOCH** (`1970-01-01T00:00:00`). This is due to the way netCDF files store time (int or float, not strings or datetime).   

# Uploading netCDF to Synoptic S3 Examples (available Mar. 2024)

The Data Providers will upload their netCDF files to Synoptic’s S3 bucket endpoint.  This will enable a trigger based processing of the files in real time, converting them to BUFR and submitting them to the Global Broker to signal to all subscribers that the data is ready to download. **Please note this will NOT be available until March 2024**. The S3 bucket directory structure is:

**operatorID/airframeID/YYYY/MM/**

Please note that this directory structure must be adhered to for successful processing of the data. Below is an example of how to upload data to Synoptic’s S3 bucket. The access key id, secret access key, and bucket name are specific to Synoptic’s S3 bucket. This uses `boto3`, an Amazon managed python package. Please first install `boto3` if you haven't already:

`pip install boto3`

or 

`conda install -c anaconda boto3`

Please do not redistribute these keys to others outside of the project. Please note the structure of the s3_filepath object in the Python script below, as this will dictate precisely where the file sits in the S3 bucket. 

The example script on how to upload an individual file [can be found here](upload_to_synoptic_s3.py)
