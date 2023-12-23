from aws_cdk import (
    # Duration,
    NestedStack,
    aws_ec2 as ec2, RemovalPolicy, )
from constructs import Construct


class SecurityGroupsNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc,
                 game_port: int,
                 query_port: int,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                              vpc=vpc,
                                              description="GamePorts",
                                              allow_all_outbound=False
                                              )
        my_security_group.apply_removal_policy(RemovalPolicy.DESTROY)

        my_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.udp(game_port), "Game port")
        my_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.udp(query_port), "Query port")
