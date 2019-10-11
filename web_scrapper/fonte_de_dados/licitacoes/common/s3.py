# -*- coding: utf-8 -*-
from botocore.exceptions import ClientError
from common.settings import Settings
import logging
import boto3
import os

class s3:
    def __init__(self):
        self.settings = Settings()
        logging.debug('Conectando ao S3...')
        try:
            self.client = boto3.client(
                's3',
                aws_access_key_id=self.settings.AWS_ACESS_KEY,
                aws_secret_access_key=self.settings.AWS_SECRET_ACESS_KEY
            )
        except ClientError as e:
            logging.error('Erro ao conectar ao s3: ' + e)


    def upload(self, filepath, destination):
        try:
            response = self.client.upload_file(filepath, self.settings.AWS_BUCKET, destination)
        except ClientError as e:
            logging.error(e)


    def listObjects(self):
        logging.info('Listando objetos para: ' + self.settings.AWS_BUCKET)
        for key in self.client.list_objects(Bucket=self.settings.AWS_BUCKET)['Contents']:
            logging.info(key['Key'])    