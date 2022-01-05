import logging

import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct


class GameserverStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger = logging.getLogger()

        # TODO deploy infra for hosting service
        # Add Metric-Based Auto-Scaling to an ApplicationLoadBalancedFargateService
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecs_patterns/README.html#add-metric-based-auto-scaling-to-an-applicationloadbalancedfargateservice

        vpc = ec2.Vpc(self, "VPC")

        cluster = ecs.Cluster(self, "Cluster",
                              vpc=vpc
                              )

        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
                                                                                           cluster=cluster,
                                                                                           memory_limit_mib=1024,
                                                                                           desired_count=1,
                                                                                           cpu=512,
                                                                                           task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                                                               image=ecs.ContainerImage.from_registry(
                                                                                                   "httpd")
                                                                                           )
                                                                                           )

        scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=5
        )

        scalable_target.scale_on_cpu_utilization("CpuScaling",
                                                 target_utilization_percent=50
                                                 )

        scalable_target.scale_on_memory_utilization("MemoryScaling",
                                                    target_utilization_percent=50
                                                    )
