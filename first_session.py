import boto3 as bt

# Retrieve the list of existing buckets
s3 = bt.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'{bucket["Name"]}')