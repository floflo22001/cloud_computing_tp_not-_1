import json
import boto3
import os

from cdktf import App
from main import MyStack

# Access queue URLs
queue1_url = os.environ.get('QUEUE1_URL')
queue2_url = os.environ.get('QUEUE2_URL')


QUEUE_URL = queue1_url
RESULTS_QUEUE_URL = queue2_url

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    try:    
        message_body = json.loads(event['Records'][0]['body'])

        # Extracting parameters
        num1 = message_body['number1']
        num2 = message_body["number2"]
        operation = message_body["operation"]

        # Check if required parameters are provided
        if num1 is None or num2 is None or operation is None:
            raise ValueError('Missing required parameters')

        # Convert parameters to integers
        num1 = int(num1)
        num2 = int(num2)

        # Performing the operation
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else :
                raise ValueError('Cannot divide by 0 !') 
        else:
            raise ValueError('Invalid operation')

        # Sending the result to the results queue
        response = sqs.send_message(
            QueueUrl=RESULTS_QUEUE_URL,
            MessageBody=json.dumps({'result': result, 'status': 'success'})
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'result': result, 'status': 'success'})
        }
    except Exception as e:
        # Sending error status to the results queue
        response = sqs.send_message(
            QueueUrl=RESULTS_QUEUE_URL,
            MessageBody=json.dumps({'error': str(e), 'status': 'error'})
        )

        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'status': 'error'})
        }