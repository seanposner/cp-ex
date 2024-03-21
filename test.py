import json
import boto3
import requests

# Service
FLASK_ENDPOINT = 'http://localhost:5000/publish'

# SQS and S3 configuration
AWS_ENDPOINT_URL = 'http://localhost:4566'
QUEUE_NAME = 'sqs'
S3_BUCKET_NAME = 'main'

# Test paylaod
data = {
    "token": "$DJISA45ex3RtYr",
    "payload": {
        "field1": "value1",
        "field2": "value2",
        "field3": "value3",
        "field4": "value4"
    }
}

# Flas POST
response = requests.post(FLASK_ENDPOINT, json=data)
print("Response from Flask app:", response.json())

# Setup client
sqs = boto3.client('sqs', endpoint_url=AWS_ENDPOINT_URL,
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')
s3 = boto3.client('s3', endpoint_url=AWS_ENDPOINT_URL,
                  region_name='us-east-1',
                  aws_access_key_id='test',
                  aws_secret_access_key='test')

# Function to check messages in sqs
def check_sqs_for_message(queue_name):
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    if 'Messages' in messages:
        return True
    else:
        return False

# Check SQS messages in correct queue
message_in_sqs = check_sqs_for_message(QUEUE_NAME)
print("Message found in SQS:", message_in_sqs)
