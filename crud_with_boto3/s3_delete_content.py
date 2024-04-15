import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Bucket name
bucket_name = 'tech257-ajhar-test-boto3'

# File to delete
file_key = 'test.txt'

# Delete file
s3.delete_object(Bucket=bucket_name, Key=file_key)
