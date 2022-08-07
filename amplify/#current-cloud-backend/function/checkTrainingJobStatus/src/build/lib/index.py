import json
import boto3
import helper

# Get SSM 
ssm = boto3.client('ssm')

# Get SM 
sm = boto3.client('sagemaker', region_name = 'ap-southeast-1')

# Get DB
TABLE_NAME = 'ppaModel-test'
db = boto3.resource('dynamodb')
table = db.Table(TABLE_NAME)

def lambda_handler(event, context):
    # TODO implement
    # From create_training_job
    model_name = event['model_name']
    try:
        response = sm.describe_training_job(
            TrainingJobName = model_name
        )
    except Exception as e:
        print(e)
        print('Unable to describe training job.')
        raise(e)
    
    params = {}
    
    status = response['TrainingJobStatus']
    creation_time = response['CreationTime']
    
    params['trainingJobName'] = model_name
    params['trainingJobStatus'] = status
    params['trainingJobCreationTime'] = creation_time.strftime("%Y-%m-%d %H:%M:%S")
    
    model_data_url = None
    if status == 'Completed':
        s3_output_path = response['OutputDataConfig']['S3OutputPath']
        model_data_url = s3_output_path + '/' + model_name + '/output/model.tar.gz'
        training_start_time = response['TrainingStartTime']
        training_end_time = response['TrainingEndTime']
        params['trainingJobModelDataUrl'] = model_data_url
        params['trainingJobStartTime'] = training_start_time.strftime("%Y-%m-%d %H:%M:%S")
        params['trainingJobEndTime'] = training_end_time.strftime("%Y-%m-%d %H:%M:%S")
    elif status == "Failed":
        failure_reason = response['FailureReason']
        params['trainingJobFailureReason'] = failure_reason

    key = {
        "model_name": model_name
    }
    
    ddbh.update_item(key, params)
    
    result = {
        "model_name": model_name,
        "status": status,
        "model_data_url": model_data_url
    }
    return result