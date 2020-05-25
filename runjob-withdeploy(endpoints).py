# S3 prefix
from sagemaker.predictor import csv_serializer
from time import gmtime, strftime
import sagemaker as sage
from sagemaker import get_execution_role
import pandas as pd
import numpy as np
import os
import re
import boto3
prefix = 'DEMO2020-SGDC-keyword-intent'

# Define IAM role


#role = get_execution_role()
role = 'SageMakerRole'

sess = sage.Session()

WORK_DIRECTORY = 'data'

data_location = sess.upload_data(WORK_DIRECTORY, key_prefix=prefix)


account = sess.boto_session.client('sts').get_caller_identity()['Account']
region = sess.boto_session.region_name
image = '{}.dkr.ecr.{}.amazonaws.com/sagemaker-sgdc-classifier:latest'.format(
    account, region)

tree = sage.estimator.Estimator(image,
                                role, 1, 'ml.c4.2xlarge',
                                output_path="s3://{}/output".format(
                                    sess.default_bucket()),
                                sagemaker_session=sess)

tree.fit(data_location)


predictor = tree.deploy(1, 'ml.m4.xlarge', serializer=csv_serializer)

print("Deployed")
