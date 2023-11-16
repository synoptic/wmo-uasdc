# WMO UASDC 

This is the central repository for the [World Meteorological Organization Uncrewed Aircraft System Demonstration Campaign project](https://community.wmo.int/en/uas-demonstration). In this repository, you'll find a collection of code, example files, and documentation related to the campaign. 

### The UASDC Pipeline

Synoptic Data PBC is responsible for converting UASDC Provider netCDF data to BUFR and sharing these datasets to the subscribed data users via the WIS2.0 Global Broker. This will be an automated pipeline existing within AWS. Therefore, it is **imperative that individual data providers take it upon themselves to ensure the proper formatting and standardization of their unique netCDF files**. 

# [Converting Raw UAS Data to netCDF](raw_uas_to_netCDF/)

**A necessary step for UASDC Data Providers is converting their unique individual files into the UASDC standardized netCDF file**. It's imperitive that each netCDF file adhere's to the variable naming convention, the standard units, and the standard file naming structure. Please find the standardized information for the netCDF files [here](raw_uas_to_netCDF/). 

   [Example raw UAS to netCDF Conversion Script](raw_uas_to_netCDF/raw_csv_to_netCDF.py)

   [Standardized netCDF Example File](nc2bufr/UASDC_operatorID_airframeID_processingLevel_20230327030016Z.nc)

# [Converting netCDF Data to BUFR](nc2bufr)

Synoptic Data will handle this part of the data pipeline. Each provider will only be responsible for handling the generation of a netCDF file that will be subsequently sent to Synoptic via the `boto3` python module ([example script can be found here](raw_uas_to_netCDF/upload_to_synoptic_s3.py)]). However, if an individual provider wants to verify that the netCDF to BUFR conversion for their data will be correct, please follow the instructions found [here](nc2bufr/). 

## Notes
- If coding support is needed, please refer to the WMO UASDC slack channel - the more activity the better!



