import boto3 as bt3

# Initialize the S3 client
s3 = bt3.client('s3')

# Step 1: Create an S3 bucket (replace 'your-unique-bucket-name' with your desired bucket name)
bucket_name = 'clement-1234'
image_path = 'dog.jpg'
object_name = 'dog.jpg'

try:
    s3.create_bucket(Bucket=bucket_name)
# Step 2: Upload an image to the bucket

# image_path: This is the source of the image on the local computer.
# bucket_name: the name of the S3 bucket where you want to upload the file.
# object_name: Sthe name you want to give the image after upload to the s3 bucket

    s3.upload_file(image_path, bucket_name, object_name)
    # s3.put_bucket_acl(Bucket=bucket_name,ACL='public-read')
    # Step 3: changing the object's ACL (Access Control List) to make it public
    s3.put_object_acl(Bucket=bucket_name, Key=object_name, ACL='public-read')

except Exception as e:
    # Printing the exception when it occurs
    print(f"An exception occured{e}")
