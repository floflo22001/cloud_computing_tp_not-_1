import json
import boto3
import os

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/381492138073/queue1"
RESULTS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/381492138073/queue2"

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    try:    

        # Extracting parameters
        num1 = event.get("number1")
        num2 = event.get("number2")
        operation = event.get("operation")

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