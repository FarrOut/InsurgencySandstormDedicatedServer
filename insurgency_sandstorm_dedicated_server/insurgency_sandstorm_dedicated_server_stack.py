from aws_cdk import (
    # Duration,
    CfnOutput,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
from insurgency_sandstorm_dedicated_server.containers.ecs_fargate_taskdefinition_nestedstack import EcsFargateTaskDefinitionNestedStack

from insurgency_sandstorm_dedicated_server.containers.ecs_nestedstack import EcsNestedStack
from insurgency_sandstorm_dedicated_server.networking.application_load_balancer_nestedstack import LoadBalancerNestedStack
from insurgency_sandstorm_dedicated_server.networking.vpc_nestedstack import VpcNestedStack
from insurgency_sandstorm_dedicated_server.security.security_groups_nestedstack import SecurityGroupsNestedStack
from insurgency_sandstorm_dedicated_server.service.service_nestedstack import ServiceNestedStack


class InsurgencySandstormDedicatedServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 game_port: int = 12345,
                 query_port: int = 54321,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        net = VpcNestedStack(self, "VpcStack", removal_policy=removal_policy)
        vpc = net.vpc

        SecurityGroupsNestedStack(self, "SecurityGroupNestedStack", vpc=vpc,
                                  game_port=game_port, query_port=query_port, removal_policy=removal_policy)

        ecs = EcsNestedStack(self, "EcsStack", vpc=vpc,
                             removal_policy=removal_policy,)
        self.cluster = ecs.cluster

        CfnOutput(self, 'ClusterArn', value=self.cluster.cluster_arn,
                  description='The Amazon Resource Name (ARN) that identifies the cluster.')
        CfnOutput(self, 'ClusterName', value=self.cluster.cluster_name,
                  description='The name of the cluster.')

        load_balancer = LoadBalancerNestedStack(self, 'LoadBalancerNestedStack',
                                                internet_facing=True,
                                                vpc=vpc,
                                                removal_policy=removal_policy).alb

        CfnOutput(self, "LoadBalancerDnsName", value=load_balancer.load_balancer_dns_name,
                  description='The DNS name of this load balancer.')        

        task_definition = EcsFargateTaskDefinitionNestedStack(
            self, 'EcsFargateTaskDefinitionNestedStack',
            game_port,
            query_port,
        ).task_definition

        load_balanced_fargate_service = ServiceNestedStack(self, 'ApplicationLoadBalancedFargateServiceNestedStack',
                                                           cluster=self.cluster,
                                                           load_balancer=load_balancer,
                                                           task_definition=task_definition,
                                                           )
