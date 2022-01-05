import json
import logging

import boto3
from aws_cdk import (
    Stack, CfnOutput,
    aws_secretsmanager as secretsmanager,
)
from aws_cdk.aws_secretsmanager import Secret
from aws_cdk.custom_resources import AwsCustomResource, AwsCustomResourcePolicy, PhysicalResourceId
from aws_cdk.pipelines import CodePipelineSource, CodePipeline, ShellStep
from constructs import Construct

from sandpipe.manufacturing.bake_stage import BakeStage


class SandpipeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger = logging.getLogger()

        connection_secret = Secret.from_secret_name_v2(self, "GitHubConnectionSecret",
                                                       'GitHub/FarrOut/connection')

        secretsmanager_ = boto3.client('secretsmanager')

        # # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
        connection_secret_value = json.loads(secretsmanager_.get_secret_value(
            SecretId='GitHub/FarrOut/connection',
        )['SecretString'])
        connection_arn_ = connection_secret_value['FarrOut']

        CfnOutput(self, 'ConnectionArn',
                  value=connection_arn_,
                  )

        github_source = CodePipelineSource.connection(
            "FarrOut/InsurgencySandstormDedicatedServer", "feature/image_oven",
            connection_arn=connection_arn_,
        )

        if github_source is None:
            logger.warning('Unable to retrieve GitHub Connection!')
        else:
            logger.info('Found GitHub Connection.')

        pipeline = CodePipeline(self, "sandpipe",
                                pipeline_name="sandpipe",
                                cross_account_keys=True,
                                synth=ShellStep("Synth",
                                                input=github_source,
                                                install_commands=["npm install -g aws-cdk",
                                                                  'python -m pip install --upgrade pip',
                                                                  "python -m pip install -r requirements.txt", ],
                                                commands=["cdk synth"]
                                                ),
                                # Turn this on because the pipeline uses Docker image assets
                                docker_enabled_for_self_mutation=True
                                )

        baking = BakeStage(self, 'BakeStage', source=github_source)
        pipeline.add_stage(baking)
