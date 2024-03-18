'''
This script is meant as an instructional example of how to upload a file to an S3 bucket using the boto3 library.
Note you will need to have the boto3 library installed to run this script, and replace the placeholders with your own values.
'''
import boto3

# access key sent separately 
aws_access_key_id = ""
# secret access key sent separately
aws_secret_access_key = ""
# bucket name
bucket_name = "provided-bucket-name"
# path to file
local_filepath = "../nc2bufr/UASDC_operatorID_airframeID_20230327025804Z.nc"
# appropriate prefix syntax for storage in s3 entry bucket
s3_filepath = "operatorID/airframeID/processingLevel/YYYY/MM/operatorID_airframeID_20230327025804Z.nc"
# or just operatorID for the prefix, ie
# s3_filepath = "operatorID/operatorID_airframeID_20230327025804Z.nc"

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Upload the file to the S3 bucket
try:
    s3.upload_file(local_filepath, bucket_name, s3_filepath)
    print(f"File {local_filepath} uploaded to {bucket_name}/{s3_filepath}")
except Exception as e:
    print(f"An error occurred: {e}")

# Listing all files in the s3 bucket
try:
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        print("Files in the bucket:")
        for item in response['Contents']:
            print(item['Key'])
    else:
        print("No files found in the bucket.")
except Exception as e:
    print(f"Failed to list files in the bucket: {e}")
