from abc import ABC

import boto3

from semantic_ai.connectors.base import BaseConnectors


class AWSS3(BaseConnectors, ABC):

    def connect(self,
                aws_access_key_id,
                aws_secret_access_key,
                bucket_name
                ):
        s3_cli = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        return s3_cli.Bucket(bucket_name)
