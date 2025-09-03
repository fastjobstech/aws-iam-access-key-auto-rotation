# (c) 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
# This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
# https://aws.amazon.com/agreement/ or other written agreement between Customer
# and Amazon Web Services, Inc.

"""Config.

Provides configuration for the application.
"""

import os
from dataclasses import dataclass

# Logging configuration
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)


@dataclass
class Config:
    """Configuration for the application."""

    # The IAM Role Session Name
    roleSessionName = os.getenv('RoleSessionName')

    # Flag- If lambda is running  in VPC
    runLambdaInVPC = str(os.getenv('RunLambdaInVPC')).lower() == 'true'

    awsAccountName = os.getenv('AWSAccountName')
    notifyEmailAddress = os.getenv('NotifyEmailAddress')
