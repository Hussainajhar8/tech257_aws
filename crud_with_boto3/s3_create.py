import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Bucket name
bucket_name = 'tech257-ajhar-test-boto3'

# Create bucket
s3.create_bucket(Bucket=bucket_name)
