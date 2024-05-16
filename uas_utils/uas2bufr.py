# Copyright 2005- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

# Description: How to encode UAS netCDF dataset into BUFR

from __future__ import print_function
import datetime
import traceback
import numpy as np
import sys
from datetime import datetime, timedelta, date
from netCDF4 import Dataset
from eccodes import *
import re
import os
np.set_printoptions(threshold=np.inf)
import logging


def validate_filename(filepath):
    # Extract the base filename from the filepath
    filename = os.path.basename(filepath)
    
    # Check for the UASDC prefix
    if not re.match(r'^UASDC_', filename):
        raise ValueError(f"Filename does not start with 'UASDC_': {filename}")
    
    # Check for exactly 3 digits for the Operator ID
    if not re.match(r'^UASDC_\d{3}_', filename):
        raise ValueError(f"Filename does not have exactly 3 digits for the Operator ID: {filename}")
    
    # Check for 1 to 5 alphanumeric characters for the airframe ID after the second underscore
    part_after_second_underscore = filename.split('_', 2)[2] if len(filename.split('_', 2)) > 2 else ''
    if not re.match(r'^[a-zA-Z0-9]{1,5}_', part_after_second_underscore):
        raise ValueError(f"Filename does not have 1 to 5 alphanumeric characters for the Airframe ID: {filename}")
    
    # Check for the date and time format followed by 'Z.nc'
    if not re.match(r'^UASDC_\d{3}_[a-zA-Z0-9]{1,5}_\d{8}\d{6}Z\.nc$', filename):
        raise ValueError(f"Filename does not end with a valid date, time format, and 'Z.nc': {filename}")

def get_attr_or_nan(obj, attr_name, postprocess_func=None):
    try:
        value = obj.getncattr(attr_name)
        if postprocess_func:
            return postprocess_func(value)
        return value
    except AttributeError:
        return np.nan

def get_var_or_nan(obj, var_name, postprocess_func=None):
    try:
        value = obj.variables[var_name][:]
        if postprocess_func:
            return postprocess_func(value)
        return value
    except KeyError:
        print(f"Warning: {var_name} not found in dataset, note that standardized variable names have been updated as of 12/20/2023")
        return np.nan

def check_missing_double(uas2Dict_read, variable_name):
    try:
        print(variable_name)
        # Attempt to access the data for the specified variable
        data = uas2Dict_read[variable_name][:]
        # Check if the data is a masked array and unmask it, filling missing values with np.nan
        if np.ma.isMaskedArray(data):
            return data.filled(np.nan)
        else:
            return data
    except Exception as e:
        # If an error occurs, return the specified code
        return CODES_MISSING_DOUBLE

def check_missing_long(uas2Dict_read, variable_name):
    try:
        # Attempt to access the data for the specified variable
        return uas2Dict_read[variable_name][:]
    except Exception as e:
        # If an error occurs, return the specified code
        return CODES_MISSING_LONG

def read_netcdf(nc_filename):

    try:
        validate_filename(nc_filename)
    except ValueError as e:
        print(e)

    uas = Dataset(nc_filename, 'r')
    
    uas2Dict={}

    uas2Dict['platform_name'] = get_attr_or_nan(uas, 'platform_name', lambda x: x.replace("-", ""))
    uas2Dict['time'] = get_var_or_nan(uas, 'time')
    uas2Dict['numSubsets'] = len(uas2Dict['time'])
    uas2Dict['longitude'] = get_var_or_nan(uas, 'lon')
    uas2Dict['latitude'] = get_var_or_nan(uas, 'lat')
    uas2Dict['airTemperature'] = get_var_or_nan(uas, 'air_temperature')
    uas2Dict['relativeHumidity'] = get_var_or_nan(uas, 'relative_humidity')
    uas2Dict['mixingRatio'] = get_var_or_nan(uas, 'humidity_mixing_ratio')
    uas2Dict['pressure'] = get_var_or_nan(uas, 'air_pressure')
    if np.isnan(uas2Dict['pressure']).all() == True:
        uas2Dict['pressure'] = get_var_or_nan(uas, 'pressure')
        if np.isnan(uas2Dict['pressure']).all() == False:
            print("Warning! The variable name for pressure has been changed to air_pressure. Please adjust the name in your netCDF file!")

    uas2Dict['windSpeed'] = get_var_or_nan(uas, 'wind_speed')
    uas2Dict['windDirection'] = get_var_or_nan(uas, 'wind_direction')
    uas2Dict['height'] = get_var_or_nan(uas, 'altitude')
    uas2Dict['dewpointTemperature'] = get_var_or_nan(uas, 'dew_point_temperature')
    uas2Dict['geopotentialHeight'] = get_var_or_nan(uas, 'geopotential_height')
    uas2Dict['nonCoordinateGeopotential'] = get_var_or_nan(uas, 'non_coordinate_geopotential')
    uas2Dict['meanTurbulenceIntensityEddyDissipationRate'] = get_var_or_nan(uas, 'eddy_dissipation_rate')
    uas2Dict['turbulentKineticEnergy'] = get_var_or_nan(uas, 'turbulent_kinetic_energy')

    ## The product time is in units
    units_time=getattr(uas.variables['time'], 'units')
    mytime = units_time.split(" ")
    mytime1= (mytime[2].split('-'))
    syear=mytime1[0]
    smonth=mytime1[1]
    mytime2=mytime1[2].split(':')
    sday=mytime2[0][:2]
    shour=mytime2[0][3:5]
    smin=mytime2[1]
    ssec=mytime2[2][:2]

    uas2Dict['syear']=int(syear)
    uas2Dict['smonth']=int(smonth)
    uas2Dict['sday']=int(sday)
    uas2Dict['shour']=int(shour)
    uas2Dict['smin']=int(smin)
    uas2Dict['ssec']=int(ssec)

    uas.close()
    return uas2Dict


def set_codes(ibufr, key, data):
    # If data is missing, it cannot be set with codes_set_array
    if data is CODES_MISSING_DOUBLE:
        codes_set(ibufr, key, CODES_MISSING_DOUBLE)
    else:
        codes_set_array(ibufr, key, data)


def uas2bufr(nc_filename, bufr_filename=None):
    uas2Dict_read=read_netcdf(nc_filename)
    nc_basename = os.path.basename(nc_filename)
    # UASDC_operatorID_airframeID_processingLevel_YYYYMMDDHHMMSSZ.nc
    operatorID = nc_basename.split('_')[1]
    airframeID = nc_basename.split('_')[2]
    processingLevel = nc_basename.split('_')[3]


    dates =[  datetime(uas2Dict_read['syear'],
                       uas2Dict_read['smonth'],
                       uas2Dict_read['sday'],
                       uas2Dict_read['shour'],
                       uas2Dict_read['smin'],
                       uas2Dict_read['ssec'])+timedelta(seconds=float(s)) for s in uas2Dict_read['time']]

    year = [d.year for d in dates]
    month = [d.month for d in dates]
    day = [d.day for d in dates]
    hour = [d.hour for d in dates]
    minute = [d.minute for d in dates]
    # second=[ (d.second+ d.microsecond/1.0e6)  for d in dates]
    second = [d.second for d in dates]

    #encoding into BUFR
    output_filename = f"{nc_basename.split('.')[0]}.bufr" if bufr_filename is None else bufr_filename
    fbufrout = open(output_filename, 'wb')

    ibufr=codes_bufr_new_from_samples('BUFR4')
    codes_set(ibufr, 'masterTableNumber', 0)
    codes_set(ibufr, 'bufrHeaderSubCentre', 0)
    codes_set(ibufr, 'bufrHeaderCentre', 98)
    codes_set(ibufr, 'updateSequenceNumber', 0)
    codes_set(ibufr, 'dataCategory', 2)
    codes_set(ibufr, 'internationalDataSubCategory', 255)
    codes_set(ibufr, 'masterTablesVersionNumber', 39)
    #codes_set(ibufr, 'masterTablesVersionNumber', 41)
    codes_set(ibufr, 'localTablesVersionNumber', 0)
    codes_set(ibufr, 'typicalYear',int(year[0]))
    codes_set(ibufr, 'typicalMonth',int(month[0]))
    codes_set(ibufr, 'typicalDay',int(day[0]))
    codes_set(ibufr, 'typicalHour',int(hour[0]))
    codes_set(ibufr, 'typicalMinute',int(minute[0]))
    codes_set(ibufr, 'typicalSecond',int(second[0]))

    codes_set(ibufr, 'observedData', 1)

    codes_set(ibufr, 'numberOfSubsets', uas2Dict_read['numSubsets'])

    codes_set(ibufr, 'compressedData', 1)
    unexpandedDescriptors =[301150,12103,7004,10003,7002,7009,1008,1095,301011,301013,301021,1013,8009,7010,33003,11001,11002,12101,2170,201135,202130,13003,202000,201000,201144,202133,13002,202000,201000,11073,11075]
    codes_set_array(ibufr, 'unexpandedDescriptors', unexpandedDescriptors)

    # below will be valid when master bufr table 41 is released
    #unexpandedDescriptors =311013
    #codes_set(ibufr, 'unexpandedDescriptors', unexpandedDescriptors)
    codes_set(ibufr, 'wigosIdentifierSeries', CODES_MISSING_LONG)
    codes_set(ibufr, 'wigosIssuerOfIdentifier', CODES_MISSING_LONG)
    codes_set(ibufr, 'wigosIssueNumber', CODES_MISSING_LONG)
    codes_set(ibufr, 'wigosLocalIdentifierCharacter','')
    codes_set(ibufr, 'observerIdentification','')
    # maximum 8 characters
    codes_set(ibufr, 'aircraftRegistrationNumberOrOtherIdentification', str(airframeID)[0:8])
    # maximum 4 characters
    codes_set(ibufr, 'observerIdentification', str(operatorID)[0:4])

    set_codes(ibufr, 'year', year)
    set_codes(ibufr, 'month', month)
    set_codes(ibufr, 'day', day)
    set_codes(ibufr, 'hour', hour)
    set_codes(ibufr, 'minute', minute)
    set_codes(ibufr, 'second', second)
    set_codes(ibufr, 'longitude', uas2Dict_read['longitude'][:])
    set_codes(ibufr, 'latitude', uas2Dict_read['latitude'][:])
    set_codes(ibufr, 'height', uas2Dict_read['height'][:])

    set_codes(ibufr, 'windDirection', check_missing_double(uas2Dict_read, 'windDirection'))
    set_codes(ibufr, 'windSpeed', check_missing_double(uas2Dict_read, 'windSpeed'))
    set_codes(ibufr, 'airTemperature', check_missing_double(uas2Dict_read, 'airTemperature'))
    set_codes(ibufr, 'relativeHumidity', check_missing_double(uas2Dict_read, 'relativeHumidity'))
    set_codes(ibufr, 'mixingRatio', check_missing_double(uas2Dict_read, 'mixingRatio'))
    set_codes(ibufr, 'turbulentKineticEnergy', check_missing_double(uas2Dict_read, 'turbulentKineticEnergy'))
    set_codes(ibufr, 'meanTurbulenceIntensityEddyDissipationRate',
              check_missing_double(uas2Dict_read, 'meanTurbulenceIntensityEddyDissipationRate'))
    set_codes(ibufr, 'geopotentialHeight', check_missing_double(uas2Dict_read, 'geopotentialHeight'))
    set_codes(ibufr, 'dewpointTemperature', check_missing_double(uas2Dict_read, 'dewpointTemperature'))
    set_codes(ibufr, 'pressure', check_missing_double(uas2Dict_read, 'pressure'))
    set_codes(ibufr, 'nonCoordinateGeopotential', check_missing_double(uas2Dict_read, 'nonCoordinateGeopotential'))

    codes_set(ibufr, 'pack', 1)
    codes_write(ibufr, fbufrout)

    codes_release(ibufr)
    fbufrout.close()
    return output_filename


def main():
    if len(sys.argv) < 2:
        print('Usage: ', sys.argv[0], ' netCDF_input_filename', file=sys.stderr)
        sys.exit(1)
 
    nc_filename = sys.argv[1]

    
    try:
        uas2bufr(nc_filename)

    except ValueError as ve :
        traceback.print_exc(file=sys.stdout)
        logging.error(ve.message) 
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

        return 1

if __name__ == "__main__":
    sys.exit(main())
