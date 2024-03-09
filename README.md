# WMO UASDC

This is the central repository for
the [World Meteorological Organization Uncrewed Aircraft System Demonstration Campaign project](https://community.wmo.int/en/uas-demonstration).
In this repository, you'll find a collection of code, example files, and documentation related to the campaign.
Please review the [UAS-DC Data Policy](https://community.wmo.int/en/uas-demonstration/data-policy) for additional
information and definitions.

## The UASDC Data Pipeline

Synoptic Data PBC is responsible for converting UASDC Provider netCDF data to BUFR and sharing these datasets to the
subscribed data users via the WIS2.0 Global Broker. This will be an automated pipeline existing within AWS. Therefore,
it is **imperative that individual data providers take it upon themselves to ensure the proper formatting and
standardization of their unique netCDF files**. A basic understanding of python
and [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html) is necessary.

### Data Pipeline Overview

![pipeline diagram](uasdc_pipeline_diagram.png)
As noted, netCDF files will be automatically converted to BUFR files on upload to the Entry S3 bucket. If successfully
converted,
the generated *.bufr* file AND the original _.nc_ file will be placed in the output/product S3 bucket. A status file
will
be generated and placed under the _processing_results/_ prefix of the Entry S3 bucket. Additionally, the generated
status file
will follow the naming convention of the original netCDF file and a suffix indicating the processing status of the file,
ie '*__success.txt' or '*__error.txt'.

```text
For example, a netCDF file uploaded to the entry bucket with the following name:
UASDC_operatorID_airframeID_20230327025804Z.nc
will have one of the following status files generated in the entry bucket after processing:

processing_results/operatorID/airframeID/UASDC_operatorID_airframeID_20230327025804Z__success.txt
processing_results/operatorID/airframeID/UASDC_operatorID_airframeID_20230327025804Z__error.txt
```

#### Requirements

* Python 3.6 or later
    * boto3
* AWS Access Key ID and Secret Access Key
    * These credentials will be distributed upon acknowledgment of the UASDC Data Policy.
    * Please do not redistribute these keys to others outside the project.
    * The unique names of the S3 buckets will be distributed along with the access credentials.
* Adherence to the variable naming convention, the standard units, and the standard file naming structure for the netCDF
  files. Please find the standardized information for the netCDF files [here](raw_uas_to_netCDF/).

#### Usage Notes

* Participants are only able to _Put_(upload), and _Get_(download) files from the S3 buckets.
    * Files will be overwritten if the same name is used.
* Data in the Entry S3 bucket will be automatically deleted after 7 days.
* Successfully converted files will be placed in the Product S3 bucket and will not be deleted.
* A basic example of how to utilize the credentials, upload a file to an S3 bucket, and list files in the bucket is
  provided in the [upload_to_s3.py](raw_uas_to_netCDF/upload_to_s3.py) file.

## [Converting Raw UAS Data to netCDF](raw_uas_to_netCDF/)

**A necessary step for UASDC Data Providers is converting their unique individual files into the UASDC standardized
netCDF file**. It's imperative that each netCDF file adheres to the variable naming convention, the standard units, and
the standard file naming structure. Please find the standardized information for the netCDF
files [here](raw_uas_to_netCDF/).

[Example raw UAS to netCDF Conversion Script](raw_uas_to_netCDF/raw_csv_to_netCDF.py)

[Standardized netCDF Example File](nc2bufr/UASDC_operatorID_airframeID_20230327025804Z.nc)

## [Converting netCDF Data to BUFR](nc2bufr)

Synoptic Data will handle this part of the data pipeline. While providers are only expected to upload netCDF files to be
automatically converted, if an individual provider wants to verify that the netCDF to BUFR conversion for their data
will be correct prior to processing or as a
debugging step, please follow the instructions found [here](nc2bufr/). In this way, same code that is used by the
automated pipeline is available for manual use.

## Notes

- If coding support is needed, please refer to the WMO UASDC slack channel - the more activity the better!



