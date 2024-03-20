import boto3
import time
import logging

# Configure logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# SQS and S3 client initialization (configure for LocalStack)
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566',
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')
s3 = boto3.client('s3', endpoint_url='http://localhost:4566',
                  region_name='us-east-1',
                  aws_access_key_id='test',
                  aws_secret_access_key='test')

# SQS queue name and S3 bucket name
QUEUE_NAME = 'sqs'
S3_BUCKET_NAME = 'main'

def ensure_resources():
    # Ensure SQS queue exists
    try:
        sqs.get_queue_url(QueueName=QUEUE_NAME)
    except sqs.exceptions.QueueDoesNotExist:
        sqs.create_queue(QueueName=QUEUE_NAME)

    # Ensure S3 bucket exists
    if S3_BUCKET_NAME not in [bucket['Name'] for bucket in s3.list_buckets().get('Buckets', [])]:
        s3.create_bucket(Bucket=S3_BUCKET_NAME)

def poll_sqs_and_upload_to_s3():
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    
    while True:
        messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=20)

        if 'Messages' in messages:
            for msg in messages['Messages']:
                message_body = msg['Body']
                receipt_handle = msg['ReceiptHandle']
                
                # Upload to S3
                s3.put_object(Bucket=S3_BUCKET_NAME, Key=f'uploads/{msg["MessageId"]}.txt', Body=message_body)
                
                # Delete the message from the queue after processing
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                logger.info(f"Uploaded message {msg['MessageId']} to S3 and deleted from SQS.")
        else:
            # Sleep if there are no messages to avoid flooding the log
            time.sleep(5)

if __name__ == '__main__':
    ensure_resources()
    poll_sqs_and_upload_to_s3()
