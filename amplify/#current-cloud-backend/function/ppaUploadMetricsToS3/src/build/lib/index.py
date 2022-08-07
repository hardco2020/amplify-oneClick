import json
import boto3
import tarfile
import os


def lambda_handler(event, context):
    model_name = 'default'
    if 'model_name' in event:
        model_name = event['model_name']
    
    s3_client = boto3.client('s3')
    s3_client.download_file('retrainoutput', model_name + '/output/model.tar.gz', '/tmp/model.tar.gz')
    
    file = tarfile.open('/tmp/model.tar.gz')
    # extracting file
    file.extractall('/tmp')
    file.close()
    
    #print(os.listdir('/tmp'))
    
    s3_client.upload_file('/tmp/metrics.json', 'retrainoutput', model_name + '/metrics.json')
    
    event['metrics_bucket'] = 'retrainoutput'
    event['metrics_filename'] = f'{model_name}/metrics.json'
    
    return event
