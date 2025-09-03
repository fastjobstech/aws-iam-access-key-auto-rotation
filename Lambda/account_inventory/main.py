# (c) 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
# https://aws.amazon.com/agreement/ or other written agreement between Customer
# and Amazon Web Services, Inc.

"""Account Inventory Handler.

This module provides the functionality to dynamically query AWS Organizations 
for a full list of account IDs and emails. This script kicks off the 
access_key_auto_rotation function.
"""

import boto3
import os
import json
import logging

from config import Config, log

config = Config()

# setup script logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# AWS Lambda Client
lambda_client = boto3.client('lambda')


# main Python Function, parses events sent to lambda
def lambda_handler(event, context):

    # environment Variables
    lambdaRotationFunction = os.environ['LambdaRotationFunction']

    sts_client = boto3.client('sts')
    current_account_id = sts_client.get_caller_identity()['Account']

    account_list = [{'Id': current_account_id, 'Name': config.awsAccountName, 'Email': config.notifyEmailAddress, 'Status': 'ACTIVE'}]

    # loop through all accounts and trigger the IAM Rotation Lambda
    run_lambda_function(account_list, lambdaRotationFunction)

def run_lambda_function(awsAccountArray, lambdaFunction):
    """
    Invokes the Lambda Function that evaluates key rotation.

    :return Response from Invoke command.
    """
    for account in awsAccountArray:
        # skip accounts that are suspended
        if account['Status'] != 'ACTIVE':
            continue
        jsonPayload = {
            "account": account['Id'],
            "name": account['Name'],
            "email": account['Email']
        }
        lambdaPayloadEncoded = json.dumps(jsonPayload).encode('utf-8')
        try:
            response = lambda_client.invoke(
                FunctionName=lambdaFunction, InvocationType='Event',
                Payload=lambdaPayloadEncoded)
            lambdaPayloadEncoded_str = str(lambdaPayloadEncoded)
            log.info(f'Invoked: FunctionName= {lambdaFunction},'
                     f' InvocationType=Event,'
                     f' Payload= {lambdaPayloadEncoded_str}')
        except lambda_client.exceptions.ClientError as error:
            log.error(f'Error: {error}')
    return response
