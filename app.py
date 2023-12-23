#!/usr/bin/env python3
import os

import aws_cdk as cdk
from insurgency_sandstorm_dedicated_server.image_oven_stack import ImageOvenStack

from insurgency_sandstorm_dedicated_server.insurgency_sandstorm_dedicated_server_stack import InsurgencySandstormDedicatedServerStack


app = cdk.App()

default_env = cdk.Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = cdk.Environment(account=os.getenv(
    'CDK_DEFAULT_ACCOUNT'), region='af-south-1')

InsurgencySandstormDedicatedServerStack(app, "InsurgencySandstormDedicatedServerStack",
                                        env=africa_env,
                                        removal_policy=cdk.RemovalPolicy.DESTROY,
                                        )

ImageOvenStack(app, "ImageOvenStack",
               env=africa_env,
               removal_policy=cdk.RemovalPolicy.DESTROY,
               )

app.synth()
