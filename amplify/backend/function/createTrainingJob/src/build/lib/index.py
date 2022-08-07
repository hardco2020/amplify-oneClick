import json

# Access Sagemaker and S3 and Dynamodb and SSM 
# Grab the needed function 

# Sagemaker 
sm = boto3.client('sagemaker', region_name = 'ap-southeast-1')

# SSM 
random_p = boto3.client('ssm').get_parameter(
    Name='/ppe/random'
).Parameter.Value

# S3 


def handler(event, context):
    # Remember to add json.loads() when testing on real api 
    print(event['body'])

    try:
        #S3 
        input_s3url = 's3://pretraininput' + random_p + '/training-inputs/input/data'
        output_s3url = 's3://retrainoutput' + random_p 
        model_tag = "default"
        if 'tag' in event:
            model_tag = event['tag']
        name_prefix = 'ppa'
        if 'name' in event['body']:
            name_prefix = event['body']['name']
        model_name = name_prefix + '-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Need to get the AWS account id 
        account_id = boto3.client("sts").get_caller_identity()["Account"]
        print(account_id)
        training_image = account_id + '.dkr.ecr.ap-southeast-1.amazonaws.com/gary-yolov5-train:latest'

        #training_image = event['training_image'] // specify the training_image from the account 
        

        cfg_prefix = 'cfg'
        weights_prefix = 'weights'
        images_prefix = 'images/train'
        labels_prefix = 'labels/train'
        if('images_prefix' in event['body']):
            images_prefix = event['body']['images_prefix']
        if('labels_prefix' in event):
            labels_prefix = event['body']['labels_prefix']
        
        # Create a role for training job to perform action successfully 
        role_arn = ssmh.get_parameter('/spot_bot/config/meta/role_arn')
        instance_type = 'ml.p3.2xlarge'
        if('instance_type' in event['body']):
            instance_type = event['body']['instance_type']
        
        response = sm.create_training_job(
            TrainingJobName = model_name,
            HyperParameters = {
            },
            AlgorithmSpecification = {
                'TrainingImage': training_image,
                'TrainingInputMode': 'File',
                'EnableSageMakerMetricsTimeSeries': True
            },
            RoleArn = role_arn,
            InputDataConfig = [
                {
                    'ChannelName': 'cfg',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': input_s3uri + '/' + cfg_prefix,
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    }
                },
                {
                    'ChannelName': 'weights',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': input_s3uri + '/' + weights_prefix,
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    }
                },
                {
                    'ChannelName': 'images',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': input_s3uri + '/' + images_prefix,
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    }
                },
                {
                    'ChannelName': 'labels',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': input_s3uri + '/' + labels_prefix,
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    }
                }
        
            ],
            OutputDataConfig = {
                'S3OutputPath': output_s3uri
            },
            ResourceConfig={
                'InstanceType': instance_type,
                'InstanceCount': 1,
                'VolumeSizeInGB': 30
            },
            StoppingCondition={
                'MaxRuntimeInSeconds': 86400
            },
            EnableNetworkIsolation = False,
            EnableInterContainerTrafficEncryption = False,
            EnableManagedSpotTraining = False
        )
        
        params = {
            'model_name' : model_name,
            "stage": 'training_job',
            'model_tag': model_tag
        }

        # dynamodb put action 
        # ddbh.put_item(params)
        
        result = {
            "model_name": model_name
        }
        return result
    except Exception as e:
        # raise e
        eprint('Error !!')
        eprint(e)
        # return {
        #   'statusCode': 500,
        #   'body': 'Error!!'
        # }    
    