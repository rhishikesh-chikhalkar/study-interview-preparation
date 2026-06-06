import os

import boto3
import requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ.setdefault("AWS_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID"))
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET_ACCESS_KEY"))
os.environ.setdefault(
    "AWS_DEFAULT_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

# Create S3 client with environment variables
s3_client = boto3.client("s3")


# --------------------------------------------------------------------------------
# Method 1: Presigned URLs (Upload & Download)
# --------------------------------------------------------------------------------

def generate_upload_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL for uploading a file"""
    try:
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        return presigned_url
    except ClientError as e:
        print(f"Error: {e}")
        return None


def upload_file_with_presigned_url(file_path, presigned_url):
    """Upload a file using a presigned URL"""
    try:
        with open(file_path, "rb") as file_data:
            response = requests.put(presigned_url, data=file_data)
        response.raise_for_status()
        print(f"Upload successful: {response.status_code}")
        return response
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


# Usage
bucket = "my-bucket"
file_key = "uploads/myfile.txt"
upload_url = generate_upload_presigned_url(bucket, file_key, expiration=3600)
print(f"Upload URL: {upload_url}")


def generate_download_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL for downloading a file"""
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        return presigned_url
    except ClientError as e:
        print(f"Error: {e}")
        return None


def download_file_with_presigned_url(presigned_url, save_path):
    """Download a file using a presigned URL"""
    try:
        response = requests.get(presigned_url)
        response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Download successful: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False


# Usage
bucket = "my-bucket"
file_key = "documents/myfile.txt"
download_url = generate_download_presigned_url(bucket, file_key, expiration=3600)
print(f"Download URL: {download_url}")

# download_file_with_presigned_url(download_url, "/local/path/myfile.txt")


# --------------------------------------------------------------------------------
# Method 2: Direct boto3 Client Methods (with AWS credentials)
# --------------------------------------------------------------------------------

def upload_file_direct(file_path, bucket_name, object_name):
    """
    Upload a file directly using S3 client
    Requires: AWS credentials configured
    Best for: Simple uploads, backend applications
    """
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Upload successful: {object_name}")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False


def download_file_direct(bucket_name, object_name, file_path):
    """
    Download a file directly using S3 client
    Requires: AWS credentials configured
    Best for: Simple downloads, backend applications
    """
    try:
        s3_client.download_file(bucket_name, object_name, file_path)
        print(f"Download successful: {file_path}")
        return True
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False


# Usage Example
# upload_file_direct('/local/myfile.txt', 'my-bucket', 'uploads/myfile.txt')
# download_file_direct('my-bucket', 'documents/myfile.txt', '/local/myfile.txt')


# --------------------------------------------------------------------------------
# Method 3: Using S3 Transfer Manager (for large files with progress)
# --------------------------------------------------------------------------------

from boto3.s3.transfer import S3Transfer


def upload_with_transfer(file_path, bucket_name, object_name):
    """
    Upload file using S3 Transfer Manager
    Best for: Large files, progress tracking
    """
    try:
        transfer = S3Transfer(s3_client)
        transfer.upload_file(file_path, bucket_name, object_name)
        print(f"Upload complete: {object_name}")
        return True
    except ClientError as e:
        print(f"Error: {e}")
        return False


def download_with_transfer(bucket_name, object_name, file_path):
    """
    Download file using S3 Transfer Manager
    Best for: Large files, progress tracking
    """
    try:
        transfer = S3Transfer(s3_client)
        transfer.download_file(bucket_name, object_name, file_path)
        print(f"Download complete: {file_path}")
        return True
    except ClientError as e:
        print(f"Error: {e}")
        return False


# Usage Example
# upload_with_transfer('/local/largefile.zip', 'my-bucket', 'uploads/largefile.zip')
# download_with_transfer('my-bucket', 'videos/myvideo.mp4', '/local/myvideo.mp4')


# --------------------------------------------------------------------------------
# Method 4: Using boto3 Resource Interface (higher-level abstraction)
# --------------------------------------------------------------------------------

s3_resource = boto3.resource("s3")


def upload_with_resource(file_path, bucket_name, object_name):
    """
    Upload file using S3 Resource interface
    Best for: Cleaner, more Pythonic code
    """
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.upload_file(file_path, object_name)
        print(f"Upload successful: {object_name}")
        return True
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return False


def download_with_resource(bucket_name, object_name, file_path):
    """
    Download file using S3 Resource interface
    Best for: Cleaner, more Pythonic code
    """
    try:
        bucket = s3_resource.Bucket(bucket_name)
        bucket.download_file(object_name, file_path)
        print(f"Download successful: {file_path}")
        return True
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False


# Usage Example
# upload_with_resource('/local/myfile.txt', 'my-bucket', 'uploads/myfile.txt')
# download_with_resource('my-bucket', 'documents/myfile.txt', '/local/myfile.txt')


# --------------------------------------------------------------------------------
# Method 5: Multi-part Upload (for very large files)
# --------------------------------------------------------------------------------

def multipart_upload(file_path, bucket_name, object_name, part_size=5 * 1024 * 1024):
    """
    Upload large file in multiple parts
    Best for: Files > 5GB, reliability, parallel uploads

    Args:
        file_path: Local file path
        bucket_name: S3 bucket name
        object_name: S3 object key
        part_size: Size of each part in bytes (default: 5MB)
    """
    try:
        # Initiate multipart upload
        response = s3_client.create_multipart_upload(
            Bucket=bucket_name, Key=object_name
        )
        upload_id = response["UploadId"]
        parts = []

        # Upload file in parts
        with open(file_path, "rb") as f:
            part_number = 1
            while True:
                data = f.read(part_size)
                if not data:
                    break

                part = s3_client.upload_part(
                    Bucket=bucket_name,
                    Key=object_name,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=data,
                )
                parts.append({"PartNumber": part_number, "ETag": part["ETag"]})
                part_number += 1
                print(f"Uploaded part {part_number - 1}")

        # Complete multipart upload
        s3_client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=object_name,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
        print(f"Multipart upload successful: {object_name}")
        return True
    except ClientError as e:
        print(f"Error: {e}")
        return False


def multipart_upload_abort(bucket_name, object_name, upload_id):
    """
    Abort a multipart upload (in case of failure)

    Args:
        bucket_name: S3 bucket name
        object_name: S3 object key
        upload_id: Upload ID returned from create_multipart_upload
    """
    try:
        s3_client.abort_multipart_upload(
            Bucket=bucket_name, Key=object_name, UploadId=upload_id
        )
        print(f"Multipart upload aborted: {upload_id}")
        return True
    except ClientError as e:
        print(f"Error aborting upload: {e}")
        return False


# Usage Example
# multipart_upload('/local/largefile.zip', 'my-bucket', 'uploads/largefile.zip')


# --------------------------------------------------------------------------------
# Comparison Table
# --------------------------------------------------------------------------------
# Method              | Use Case                    | Requires Credentials | Best For
# ----------------------------------------------------------------------------------
# Presigned URL       | Temporary public access     | No (URL-based)      | Sharing with non-AWS users
# Direct boto3        | Internal application access | Yes                 | Backend services, Lambda
# Transfer Manager    | Large files with progress   | Yes                 | Big uploads/downloads
# Resource API        | Higher-level abstraction    | Yes                 | Simpler code
# Multi-part          | Very large files            | Yes                 | 5GB+ files, reliability
# ----------------------------------------------------------------------------------
