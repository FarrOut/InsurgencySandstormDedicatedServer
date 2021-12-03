from aws_cdk import core as cdk
from aws_cdk.pipelines import CodePipelineSource

from sandpipe.manufacturing.oven_stack import OvenStack


class BakeStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, source: CodePipelineSource, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ovenStack = OvenStack(self, "DockerOvenStack", source)
