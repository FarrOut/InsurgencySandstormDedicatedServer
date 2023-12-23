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


class EcsFargateTaskDefinitionNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str,
            game_port: int,
            query_port: int,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            task_role: iam.IRole = None,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.task_def = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            memory_limit_mib=512,
            cpu=256,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
                cpu_architecture=ecs.CpuArchitecture.X86_64,
            ),
            # volumes=[volume_one],
            task_role=task_role,
        )

        log_group = LogGroup(
            self,
            "LogGroup",
            retention=RetentionDays.ONE_WEEK,
            removal_policy=removal_policy,
        )

        container_def = ecs.ContainerDefinition(
            self,
            "ContainerDef",
            task_definition=self.task_def,
            image=ContainerImage.from_registry(
                "andrewmhub/insurgency-sandstorm:latest"),
            port_mappings=[
                ecs.PortMapping(container_port=game_port,
                                protocol=ecs.Protocol.UDP),
                ecs.PortMapping(container_port=query_port,
                                protocol=ecs.Protocol.UDP)
            ],
            logging=ecs.AwsLogDriver(
                stream_prefix="InsurgencySanstorm",
                mode=ecs.AwsLogDriverMode.NON_BLOCKING,
                log_group=log_group,
            ),
        )

        CfnOutput(
            self,
            "ContainerName",
            description="The name of this container.",
            value=container_def.container_name,
        )
        CfnOutput(
            self,
            "ContainerPort",
            description="The port the container will listen on.",
            value=str(container_def.container_port),
        )
        CfnOutput(
            self,
            "ContainerCpu",
            description="The number of cpu units reserved for the container.",
            value=str(container_def.cpu),
        )
        CfnOutput(
            self,
            "ContainerIsEssential",
            description="Specifies whether the container will be marked essential.",
            value=str(container_def.essential),
        )
        CfnOutput(
            self,
            "ContainerImageName",
            description="The name of the image referenced by this container.",
            value=container_def.image_name,
        )

        log_driver_config = container_def.log_driver_config
        if log_driver_config is not None:
            CfnOutput(
                self,
                "ContainerLogDriver",
                description="The log driver to use for the container.",
                value=str(log_driver_config.log_driver),
            )
            CfnOutput(
                self,
                "ContainerLogDriverOptions",
                description="The configuration options to send to the log driver.",
                value=str(log_driver_config.options),
            )

        CfnOutput(self, "TaskDefinitionArn", value=self.task_definition.task_definition_arn,
                  description='The full Amazon Resource Name (ARN) of the task definition.')
