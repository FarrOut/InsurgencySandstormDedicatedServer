#!/usr/bin/env python3
import json
import os

import aws_cdk as cdk
# Environments
import boto3

from sandpipe.sandpipe_stack import SandpipeStack

env_cpt = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')

app = cdk.App()

secretsmanager_ = boto3.client('secretsmanager')


def fetch_connection_arn() -> str:
    # # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
    connection_secret_value = json.loads(secretsmanager_.get_secret_value(
        SecretId='GitHub/FarrOut/connection',
    )['SecretString'])
    connection_arn_ = connection_secret_value['FarrOut']
    return connection_arn_

SandpipeStack(app, "SandpipeStack",
              connection_arn=fetch_connection_arn(),

              # If you don't specify 'env', this stack will be environment-agnostic.
              # Account/Region-dependent features and context lookups will not work,
              # but a single synthesized template can be deployed anywhere.

              # Uncomment the next line to specialize this stack for the AWS Account
              # and Region that are implied by the current CLI configuration.

              env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
              # Uncomment the next line if you know exactly what Account and Region you
              # want to deploy the stack to. */

              # env=core.Environment(account='123456789012', region='us-east-1'),

              # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
              )

# TODO excluded while we work on the bake stage
# GameserverStack(app, "GameserverStack",
#                 env=env_cpt,
#                 )

app.synth()
