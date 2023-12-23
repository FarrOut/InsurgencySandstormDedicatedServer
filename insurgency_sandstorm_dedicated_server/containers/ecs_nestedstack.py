from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs, aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct


class EcsNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str, vpc: ec2.Vpc, container_image: ContainerImage = None,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        CfnOutput(self, 'ClusterArn', value=self.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.cluster.cluster_name,
                  description='The name of the cluster.')
