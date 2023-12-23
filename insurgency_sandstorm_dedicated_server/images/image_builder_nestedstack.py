from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2,
    aws_efs as efs, aws_imagebuilder as imagebuilder,
    aws_ecs as ecs, aws_iam as iam, aws_s3 as s3,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_logs import LogGroup, RetentionDays
from constructs import Construct

from insurgency_sandstorm_dedicated_server.storage.s3_nestedstack import S3NestedStack


class ImageBuilderNestedStack(NestedStack):
    def __init__(
            self, scope: Construct, construct_id: str,
            removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
            key_pair: str = None,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self, "Role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
                        )
        role.apply_removal_policy(removal_policy)

        instance_profile = iam.InstanceProfile(self, "InstanceProfile",
                                               role=role
                                               )
        instance_profile.apply_removal_policy(removal_policy)

        log_bucket = S3NestedStack(
            self, 'LoggingBucketStack', auto_delete_objects=True, removal_policy=removal_policy)

        cfn_infrastructure_configuration = imagebuilder.CfnInfrastructureConfiguration(self, "MyCfnInfrastructureConfiguration",
                                                                                       instance_profile_name=instance_profile.instance_profile_name,
                                                                                       name="InsungencySandstormBuildInfra",

                                                                                       # the properties below are optional
                                                                                       description="Infrastructure for building Insurgancy Sandstorm dedicated server AMIs.",

                                                                                       instance_types=['m4.large',
                                                                                                       'm5.large'],
                                                                                       key_pair=key_pair,
                                                                                       logging=imagebuilder.CfnInfrastructureConfiguration.LoggingProperty(
                                                                                           s3_logs=imagebuilder.CfnInfrastructureConfiguration.S3LogsProperty(
                                                                                               s3_bucket_name=log_bucket.bucket.bucket_name,
                                                                                               s3_key_prefix=str(
                                                                                                   self.stack_id)
                                                                                           )
                                                                                       ),
                                                                                       resource_tags={
                                                                                           "CreatedBy": str(
                                                                                               self.stack_id),
                                                                                           "Purpose": "InsurgencySandstorm"
                                                                                       },
                                                                                       #    security_group_ids=[
                                                                                       #        "securityGroupIds"],
                                                                                       #    sns_topic_arn="snsTopicArn",
                                                                                       #    subnet_id="subnetId",
                                                                                       tags={
                                                                                           "Purpose": "InsurgencySandstorm"
                                                                                       },
                                                                                       terminate_instance_on_failure=True
                                                                                       )

        cfn_distribution_configuration = imagebuilder.CfnDistributionConfiguration(self, "InsurgencySandstorm",
                                                                                   distributions=[imagebuilder.CfnDistributionConfiguration.DistributionProperty(
                                                                                       region=self.region,

                                                                                       # the properties below are optional
                                                                                       # ami_distribution_configuration=ami_distribution_configuration,
                                                                                       # container_distribution_configuration=container_distribution_configuration,
                                                                                       # fast_launch_configurations=[imagebuilder.CfnDistributionConfiguration.FastLaunchConfigurationProperty(
                                                                                       #     account_id="accountId",
                                                                                       #     enabled=False,
                                                                                       #     launch_template=imagebuilder.CfnDistributionConfiguration.FastLaunchLaunchTemplateSpecificationProperty(
                                                                                       #         launch_template_id="launchTemplateId",
                                                                                       #         launch_template_name="launchTemplateName",
                                                                                       #         launch_template_version="launchTemplateVersion"
                                                                                       #     ),
                                                                                       #     max_parallel_launches=123,
                                                                                       #     snapshot_configuration=imagebuilder.CfnDistributionConfiguration.FastLaunchSnapshotConfigurationProperty(
                                                                                       #         target_resource_count=123
                                                                                       #     )
                                                                                       # )],
                                                                                       # launch_template_configurations=[imagebuilder.CfnDistributionConfiguration.LaunchTemplateConfigurationProperty(
                                                                                       #     account_id="accountId",
                                                                                       #     launch_template_id="launchTemplateId",
                                                                                       #     set_default_version=False
                                                                                       # )],
                                                                                       # license_configuration_arns=["licenseConfigurationArns"]
                                                                                   )],
                                                                                   name="InsurgencySandstormDistributionConfig",

                                                                                   # the properties below are optional
                                                                                   # description="description",
                                                                                   # tags={
                                                                                   #     "tags_key": "tags"
                                                                                   # }
                                                                                   )

        cfn_image_recipe = imagebuilder.CfnImageRecipe(self, "InsurgencySandstormImageRecipe",
                                                       components=[imagebuilder.CfnImageRecipe.ComponentConfigurationProperty(
                                                           component_arn="componentArn",
                                                           parameters=[imagebuilder.CfnImageRecipe.ComponentParameterProperty(
                                                               name="name",
                                                               value=["value"]
                                                           )]
                                                       )],
                                                       name="InsurgencySandstormDedicatedServer",
                                                       parent_image="parentImage",
                                                       version="0.0.1a",

                                                       # the properties below are optional
                                                       additional_instance_configuration=imagebuilder.CfnImageRecipe.AdditionalInstanceConfigurationProperty(
                                                           systems_manager_agent=imagebuilder.CfnImageRecipe.SystemsManagerAgentProperty(
                                                               uninstall_after_build=False
                                                           ),
                                                           #    user_data_override="userDataOverride"
                                                       ),
                                                       #    block_device_mappings=[imagebuilder.CfnImageRecipe.InstanceBlockDeviceMappingProperty(
                                                       #        device_name="deviceName",
                                                       #        ebs=imagebuilder.CfnImageRecipe.EbsInstanceBlockDeviceSpecificationProperty(
                                                       #            delete_on_termination=False,
                                                       #            encrypted=False,
                                                       #            iops=123,
                                                       #            kms_key_id="kmsKeyId",
                                                       #            snapshot_id="snapshotId",
                                                       #            throughput=123,
                                                       #            volume_size=123,
                                                       #            volume_type="volumeType"
                                                       #        ),
                                                       #        no_device="noDevice",
                                                       #        virtual_name="virtualName"
                                                       #    )],
                                                       #    description="description",
                                                       tags={
                                                           "Purpose": "InsurgencySandstorm"
                                                       },
                                                       #    working_directory="workingDirectory"
                                                       )

        cfn_image_pipeline = imagebuilder.CfnImagePipeline(self, "InsurgencySandstormImagePipeline",
                                                           infrastructure_configuration_arn=cfn_infrastructure_configuration.attr_arn,
                                                           name="InsurgencySandstormImagePipeline",

                                                           # the properties below are optional
                                                           description="Build Insurgency Sandstorm AMI",
                                                           distribution_configuration_arn=cfn_distribution_configuration.attr_arn,
                                                           enhanced_image_metadata_enabled=False,
                                                           #    execution_role="executionRole",
                                                           image_recipe_arn=cfn_image_recipe.attr_arn,
                                                           #    image_scanning_configuration=imagebuilder.CfnImagePipeline.ImageScanningConfigurationProperty(
                                                           #        ecr_configuration=imagebuilder.CfnImagePipeline.EcrConfigurationProperty(
                                                           #            container_tags=[
                                                           #                "containerTags"],
                                                           #            repository_name="repositoryName"
                                                           #        ),
                                                           #        image_scanning_enabled=False
                                                           #    ),
                                                           #    image_tests_configuration=imagebuilder.CfnImagePipeline.ImageTestsConfigurationProperty(
                                                           #        image_tests_enabled=False,
                                                           #        timeout_minutes=123
                                                           #    ),
                                                           #    schedule=imagebuilder.CfnImagePipeline.ScheduleProperty(
                                                           #        pipeline_execution_start_condition="pipelineExecutionStartCondition",
                                                           #        schedule_expression="scheduleExpression"
                                                           #    ),
                                                           status="ENABLED",
                                                           tags={
                                                               "Purpose": "InsurgencySandstorm"
                                                           },
                                                           #    workflows=[imagebuilder.CfnImagePipeline.WorkflowConfigurationProperty(
                                                           #        on_failure="onFailure",
                                                           #        parallel_group="parallelGroup",
                                                           #        parameters=[imagebuilder.CfnImagePipeline.WorkflowParameterProperty(
                                                           #            name="name",
                                                           #            value=[
                                                           #                "value"]
                                                           #        )],
                                                           #        workflow_arn="workflowArn"
                                                           #    )]
                                                           )
