#!/usr/bin/env python3
import os

import aws_cdk as cdk

from insurgency_sandstorm_dedicated_server.insurgency_sandstorm_dedicated_server_stack import InsurgencySandstormDedicatedServerStack


app = cdk.App()
InsurgencySandstormDedicatedServerStack(app, "InsurgencySandstormDedicatedServerStack",
                                        env=cdk.Environment(account=os.getenv(
                                            'CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
                                        removal_policy=cdk.RemovalPolicy.DESTROY,
                                        )

app.synth()
