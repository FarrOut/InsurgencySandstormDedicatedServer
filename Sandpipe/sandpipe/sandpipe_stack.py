from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep



class SandpipeStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

# CodeStar connection
# arn:aws:codestar-connections:eu-west-1:595470990922:connection/c8f6dce5-bc13-479d-8015-0c3fe03b68ef

        connection_arn = 'arn:aws:codestar-connections:eu-west-1:595470990922:connection/c8f6dce5-bc13-479d-8015-0c3fe03b68ef'

        pipeline =  CodePipeline(self, "Sandpipe",
                        pipeline_name="Sandpipe",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.connection("FarrOut/InsurgencySandstormDedicatedServer", "main",
                            connection_arn=connection_arn,
                            ),
                            commands=["npm install -g aws-cdk", "cdk synth"]
                        )
                    )
