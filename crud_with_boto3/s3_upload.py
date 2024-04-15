import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Bucket name
bucket_name = 'tech257-ajhar-test-boto3'

# File to upload
file_path = 'test.txt'

# Upload file
s3.upload_file(file_path, bucket_name, 'test.txt')
