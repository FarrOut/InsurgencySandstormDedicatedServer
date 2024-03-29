from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     pipelines,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as cpactions,
                     aws_secretsmanager,
                     )
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
import boto3, json, logging


class SandpipeStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger = logging.getLogger()

        connection_secret = aws_secretsmanager.Secret.from_secret_name_v2(self, "GitHubConnectionSecret",
                                                                          'GitHub/FarrOut/connection')

        secretsmanager = boto3.client('secretsmanager')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
        connection_secret_value = json.loads(secretsmanager.get_secret_value(
            SecretId='GitHub/FarrOut/connection',
        )['SecretString'])
        connection_arn_ = connection_secret_value['FarrOut']

        if connection_secret.secret_value is None:
            logger.warning('Unable to retrieve GitHub Connection!')
        else:
            logger.info('Found GitHub Connection.')

        pipeline = CodePipeline(self, "Sandpipe",
                                pipeline_name="Sandpipe",
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.connection(
                                                    "FarrOut/InsurgencySandstormDedicatedServer", "main",
                                                    connection_arn=connection_arn_,
                                                    ),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                )
                                )