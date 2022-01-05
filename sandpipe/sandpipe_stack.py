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

    def __init__(self, scope: Construct, construct_id: str, connection_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger = logging.getLogger()

        CfnOutput(self, 'ConnectionArn',
                  value=connection_arn,
                  )

        github_source = CodePipelineSource.connection(
            "FarrOut/InsurgencySandstormDedicatedServer", "feature/image_oven",
            connection_arn=connection_arn,
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
