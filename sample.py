import json
import boto3 as bt3

# Initialize the S3 client
s3 = bt3.client('s3')

# Step 1: Create an S3 bucket (replace 'your-unique-bucket-name' with your desired bucket name)
bucket_name = 'clement-123-bucket'
image_path = 'index.html'
object_name = 'index.html'
# this is the bucket polity to make the bucket public
bucket_policy = '{"Version": "2012-10-17", "Statement": [{ "Sid": "id-1","Effect": "Allow","Principal": "*", "Action": [ "s3:PutObject","s3:PutObjectAcl","s3:GetObject","s3:GetObjectAcl"], "Resource": ["arn:aws:s3:::clement-123-bucket/*" ] } ]}'


try:
    s3.create_bucket(Bucket=bucket_name)
# Step 2: Upload an image to the bucket

# image_path: This is the source of the image on the local computer.
# bucket_name: the name of the S3 bucket where you want to upload the file.
# object_name: Sthe name you want to give the image after upload to the s3 bucket

    
    s3.delete_public_access_block(Bucket=bucket_name)
    s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
    s3.upload_file(image_path, bucket_name, object_name)
    # Step 3: changing the object's ACL (Access Control List) to make it public
    # s3.put_object_acl(Bucket=bucket_name, Key=object_name, ACL='public-read')

    # getting the object
    s3.get_bucket_policy(Bucket=bucket_name)
    s3.get_object(Bucket=bucket_name, Key=object_name)
except Exception as e:
    # Printing the exception when it occurs
    print(f"An exception occured{e}")
