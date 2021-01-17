import json
import boto3
# import requests


def read_file(bucket, file):
    s3 = boto3.client('s3')
    with open('/tmp/file.json', 'wb') as f:
        s3.download_fileobj(bucket, file, f)

    with open('/tmp/file.json') as json_file:
        data = json.load(json_file)

    print(data)


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    read_file(bucket_name, file_key)

