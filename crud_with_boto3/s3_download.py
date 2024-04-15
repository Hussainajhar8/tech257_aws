import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Bucket name
bucket_name = 'tech257-ajhar-test-boto3'

# File to download
file_path ='test.txt'

# Download file
s3.download_file(bucket_name, 'test.txt', file_path)
