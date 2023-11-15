import boto3

# access key sent separately 
aws_access_key_id = ""
# secret access key sent separately
aws_secret_access_key = ""

bucket_name = "wmo-uasdc-synoptic-bucket"

local_filepath = "UASDC_operatorID_airframeID_processingLevel_20230327030016Z.nc"  
s3_filepath = "operatorID/airframeID/processingLevel/YYYY/MM/operatorID_airframeID_processingLevel_YYYYMMDDHHMMSSZ.nc"

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

try:
    # Upload the file to the S3 bucket
    s3.upload_file(local_filepath, bucket_name, s3_filename)
    print(f"File {local_filepath} uploaded to {bucket_name}/{s3_filepath}")
except Exception as e:
    print(f"An error occurred: {e}")