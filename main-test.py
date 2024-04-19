import pytest
from cdktf import Testing
from main import MyStack  

import boto3
import json

# The tests below are example tests, you can find more information at
# https://cdk.tf/testing


class TestMain:


    def test_sqs_and_lambda():

        sqs = boto3.client('sqs', region_name='us-east-1')
       
        message_body = {"number1": 3, "number2": 4, "operation": "*"}
        message_body2 = {"number1" :6, "number2" :3, "operation" :"+"}
        message_body3 = {"number1" :3, "number2" :0, "operation" :"/"}

        response = sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/381492138073/queue1',
            MessageBody=json.dumps(message_body)
        )

        response = sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/381492138073/queue1',
            MessageBody=json.dumps(message_body2)
        )

        response = sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/381492138073/queue1',
            MessageBody=json.dumps(message_body3)
        )


if __name__ == "__main__":
    TestMain.test_sqs_and_lambda()