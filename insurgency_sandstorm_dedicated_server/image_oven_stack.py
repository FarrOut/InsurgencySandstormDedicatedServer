from aws_cdk import (
    # Duration,
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
from insurgency_sandstorm_dedicated_server.containers.ecs_fargate_taskdefinition_nestedstack import EcsFargateTaskDefinitionNestedStack

from insurgency_sandstorm_dedicated_server.containers.ecs_nestedstack import EcsNestedStack
from insurgency_sandstorm_dedicated_server.images.image_builder_nestedstack import ImageBuilderNestedStack
from insurgency_sandstorm_dedicated_server.networking.application_load_balancer_nestedstack import LoadBalancerNestedStack
from insurgency_sandstorm_dedicated_server.networking.vpc_nestedstack import VpcNestedStack
from insurgency_sandstorm_dedicated_server.security.security_groups_nestedstack import SecurityGroupsNestedStack
from insurgency_sandstorm_dedicated_server.service.service_nestedstack import ServiceNestedStack


class ImageOvenStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ImageBuilderNestedStack(self, 'ImageBuilderNestedStack', removal_policy=removal_policy)
