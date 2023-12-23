import logging

from aws_cdk import (
    # Duration,
    NestedStack,
    RemovalPolicy, aws_codedeploy as codedeploy,
    Stack, aws_elasticloadbalancingv2 as elbv2, aws_elasticloadbalancing as elb,
    aws_ec2 as ec2, CfnOutput, )
from constructs import Construct


class LoadBalancerNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, removal_policy: RemovalPolicy, internet_facing: bool = False,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.alb = elbv2.ApplicationLoadBalancer(self, "LB",
                                                 vpc=vpc,
                                                 internet_facing=internet_facing,
                                                 deletion_protection=((removal_policy == RemovalPolicy.RETAIN) or (
                                                     removal_policy == RemovalPolicy.SNAPSHOT)),
                                                 )
        self.alb.apply_removal_policy(removal_policy)

        # Outputs
        CfnOutput(self, "LoadBalancerName", value=self.alb.load_balancer_name,
                  description='The name of this load balancer.')
        CfnOutput(self, "LoadBalancerFullName", value=self.alb.load_balancer_full_name,
                  description='The full name of this load balancer.')
        CfnOutput(self, "LoadBalancerDnsName", value=self.alb.load_balancer_dns_name,
                  description='The DNS name of this load balancer.')
        CfnOutput(self, "LoadBalancerCanonicalHostedZoneId", value=self.alb.load_balancer_canonical_hosted_zone_id,
                  description='The canonical hosted zone ID of this load balancer.')
        CfnOutput(self, "LoadBalancerArn", value=self.alb.load_balancer_arn,
                  description='The ARN of this load balancer.')
