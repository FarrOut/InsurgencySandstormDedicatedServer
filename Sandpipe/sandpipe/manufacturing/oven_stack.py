from aws_cdk import (core as cdk,
                     aws_codebuild as codebuild,
                     aws_imagebuilder as imagebuilder,
                     aws_logs as logs,
                     )
from aws_cdk.pipelines import CodePipelineSource, ShellStep, CodeBuildStep


class OvenStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, source: CodePipelineSource, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Docker sample for CodeBuild
        # https://docs.aws.amazon.com/codebuild/latest/userguide/sample-docker.html

        #  kbanman / cdk-docker-pipeline-example
        # https://github.com/kbanman/cdk-docker-pipeline-example

        # Create a container image pipeline using the EC2 Image Builder console wizard
        # https://docs.aws.amazon.com/imagebuilder/latest/userguide/start-build-container-pipeline.html

        # aws-samples/aws-cdk-imagebuilder-pipeline
        # https://github.com/aws-samples/aws-cdk-imagebuilder-pipeline

        git_hub_source = codebuild.Source.git_hub(
            owner="FarrOut",
            repo="InsurgencySandstormDedicatedServer",
            webhook=True,  # optional, default: true if `webhookFilters` were provided, false otherwise
            # webhook_triggers_batch_build=True,  # optional, default is false
            # webhook_filters=[
            #     codebuild.FilterGroup.in_event_of(codebuild.EventAction.PUSH).and_branch_is(
            #         "master").and_commit_message_is("the commit message")
            # ]
        )

        CodeBuildStep("BuildDockerfile",
                      install_commands=[],
                      env={"REPOSITORY_URI": "FarrOut/InsurgencySandstormDedicatedServer"},
                      commands=["docker build -t $REPOSITORY_URI:latest ."],
                      build_environment=codebuild.BuildEnvironment(
                          # The user of a Docker image asset in the pipeline requires turning on
                          # 'dockerEnabledForSelfMutation'.
                          build_image=codebuild.LinuxBuildImage.UBUNTU_14_04_DOCKER_18_09_0,
                          privileged=True,

                      ),

                      )
