import boto3
import os
import csv
import botocore
from time import gmtime, strftime
from boto3.session import Session
import json
import pandas as pd
import io
from io import StringIO
import numpy as np

endpoint_name = input("Please input your endpoint name:\n")


def csv_formatbody(row):
    #   print("Row to Format is..", row)
    #   Need to convert csv data in from:
    #   ['setosa', '5.0', '3.5', '1.3', '0.3']
    #   TO: b'setosa,5.0,3.5,1.3,0.3'

    string_row = ','.join(str(e) for e in row)

    return string_row


access_key = '*****'
secret_key = '****'
session = Session(aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)
runtime_client = session.client('runtime.sagemaker')

df = pd.read_csv('payload.csv')
print(df)
test_file = io.StringIO()
df.to_csv(test_file, header=None, index=None)

csv_data = csv.reader(open('payload.csv', newline=''))
for row in csv_data:
    formatted_input = csv_formatbody(row)
    print('formatted_input:', formatted_input)
    invoke_endpoint_body = formatted_input.encode('utf-8')
    print("invoke_endpoint_body:", invoke_endpoint_body)
    response = runtime_client.invoke_endpoint(
        ContentType='text/csv', Body=invoke_endpoint_body, EndpointName=endpoint_name)
    print(response['Body'].read().decode())
