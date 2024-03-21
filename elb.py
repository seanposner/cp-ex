import os
import boto3
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Hard coded token
VALID_TOKEN = "$DJISA45ex3RtYr"

# SQS client init
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566',
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')

QUEUE_NAME = 'sqs'

# Ensure SQS
def ensure_sqs_queue_exists():
    try:
        return sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    except sqs.exceptions.QueueDoesNotExist:
        return sqs.create_queue(QueueName=QUEUE_NAME)['QueueUrl']

# Validate token
def validate_token(token):
    return token == VALID_TOKEN

# Validate the payload
def validate_payload(payload):
    required_fields = ['field1', 'field2', 'field3', 'field4']
    return all(field in payload for field in required_fields)

# Call to publish payload to SQS
@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.json
    token = data.get('token')
    payload = data.get('payload')

    if not validate_token(token):
        return jsonify({'error': 'Invalid token'}), 401

    if not validate_payload(payload):
        return jsonify({'error': 'Invalid payload'}), 400
    
    queue_url = ensure_sqs_queue_exists()

    # Publish to SQS
    sqs.send_message(QueueUrl=queue_url, MessageBody=str(payload))

    # Set response
    return jsonify({'message': 'Payload published successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
