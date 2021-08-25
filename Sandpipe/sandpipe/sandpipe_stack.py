from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep



class SandpipeStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        pipeline =  CodePipeline(self, "Sandpipe",
                        pipeline_name="Sandpipe",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("FarrOut/InsurgencySandstormDedicatedServer", "main"),
                            commands=["npm ci", "npm run build", "npx cdk synth"]
                        )
                    )
