import boto3
import json
import os
import mimetypes

# Configuration
BUCKET_NAME = "my-static-website-bucket-karmegtej0611030212345"  # Change to your unique bucket name
LOCAL_WEBSITE_DIR = "./website_files"  # Directory containing static files
AWS_REGION = "us-east-1"  # Change if needed

# Initialize S3 client
s3 = boto3.client("s3", region_name=AWS_REGION)

def create_s3_bucket(bucket_name):
    """Creates an S3 bucket if it doesn't exist."""
    try:
        if AWS_REGION == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )
        print(f"✅ Bucket '{bucket_name}' created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"ℹ️ Bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"❌ Error creating bucket: {e}")

def enable_website_hosting(bucket_name):
    """Enables static website hosting on the S3 bucket."""
    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}
        }
    )
    print(f"✅ Static website hosting enabled for '{bucket_name}'.")

def set_bucket_policy(bucket_name):
    """Sets public access policy for the bucket."""
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print(f"✅ Public access policy applied to '{bucket_name}'.")

def upload_files_to_s3(bucket_name, local_directory):
    """Uploads files from a local directory to S3 bucket."""
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = file  # Keep file name same in S3
            
            # Guess MIME type
            content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            
            # Upload file to S3 (No ACL, Bucket Policy is used instead)
            s3.upload_file(file_path, bucket_name, s3_key, ExtraArgs={'ContentType': content_type})
            print(f"✅ Uploaded '{file}' to S3.")

def get_website_url(bucket_name):
    """Returns the static website URL."""
    website_url = f"http://{bucket_name}.s3-website-{AWS_REGION}.amazonaws.com"
    print(f"🌍 Website URL: {website_url}")

def main():
    create_s3_bucket(BUCKET_NAME)
    enable_website_hosting(BUCKET_NAME)
    set_bucket_policy(BUCKET_NAME)  # Apply public access policy
    upload_files_to_s3(BUCKET_NAME, LOCAL_WEBSITE_DIR)
    get_website_url(BUCKET_NAME)

if __name__ == "__main__":
    main()
