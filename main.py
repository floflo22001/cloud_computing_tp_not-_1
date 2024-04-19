# Code de Florian ROUDAUT

from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, TerraformAsset, AssetType
from cdktf_cdktf_provider_aws.sqs_queue import SqsQueue
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.data_aws_caller_identity import DataAwsCallerIdentity
from cdktf_cdktf_provider_aws.lambda_event_source_mapping import LambdaEventSourceMapping
import os

import boto3

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        AwsProvider(self, "AWS", region="us-east-1")

        account_id = DataAwsCallerIdentity(self, "account_id").account_id

        code = TerraformAsset(
            self, "code",
            path="./lambda", # dossier du code
            type= AssetType.ARCHIVE
        )

        # Create the first SQS queue for event queueing
        queue1 = SqsQueue(self, "Queue1", name="queue1")


        # Create the second SQS queue for result queueing
        queue2 = SqsQueue(self, "Queue2", name="queue2")

        # Define the Lambda function
        lambda_func = LambdaFunction(
            self,
            "MyLambda",
            function_name="lambda",
            runtime="python3.8",
            role=f"arn:aws:iam::{account_id}:role/LabRole",
            filename=code.path, 
            handler="lambda_function.lambda_handler",
            environment={
                "variables": {
                    "QUEUE_URL": queue1.id,
                    "RESULTS_QUEUE_URL": queue2.id,
                    "foo": "bar"
                }
            }
        )

        # Define the Lambda event source mapping
        event_source_mapping = LambdaEventSourceMapping(
            self,
            "Queue1EventSourceMapping",
            event_source_arn=queue1.arn,  
            function_name=lambda_func.function_name,
            batch_size=1,  
            enabled=True
        )

        # Output to display the URL of the event queue
        TerraformOutput(self, "EventQueueURL", value=queue1.id)

        # Output to display the URL of the result queue
        TerraformOutput(self, "ResultQueueURL", value=queue2.id)

        # Save urls in os
        os.environ['QUEUE1_URL'] = queue1.id
        os.environ['QUEUE2_URL'] = queue2.id





app = App()
MyStack(app, "graded_lab")

app.synth()
