import json
import boto3
import sys

override_camera_template = {
    "nodeGraphOverrides": {
		"envelopeVersion": "2021-01-01",
		"packages": [],
		"nodes": [],
		"nodeOverrides": [
		    {
		        "replace": "front_door_camera",
		        "with": []
		    }
		]
	}
}

# Hack to print to stderr so it appears in CloudWatch.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, ** kwargs)

def post(event, account_id):
    print(event)
    TABLE_NAME = "PPE_Deployment_table"
    db = boto3.resource('dynamodb')
    s3 = boto3.resource('s3')
    pano_client = boto3.client('panorama')
    table = db.Table(TABLE_NAME)
    body = json.loads(event['body'])
   #print(body['Device_ID'])
   #print(body['Camera_ID'])
   #print(body['Component_Version_ID'])
   #print(body['Model_Version_ID'])
   #print(body['targetArn'])
   #print(body['deploymentName'])
   #print(body['components'])
   #print(body['deploymentPolicies'])
   #print(body['iotJobConfigurations'])
    # Use Model_Version_ID for Panorama camera list   
    cameras=body['Model_Version_ID'].split(', ')
    
    for camera in cameras:
	    override_camera_template['nodeGraphOverrides']['packages'].append({
	    	'name': '{acc_id}::{name}'.format(acc_id=account_id, name=camera),
	    	'version': '0.1'
	    })
	    override_camera_template['nodeGraphOverrides']['nodes'].append({
	    	'name': '{}'.format(camera),
	    	'interface': '{acc_id}::{name}.{name}'.format(acc_id=account_id, name=camera),
	    	'overridable': True,
	    	'overrideMandatory': False,
	    	'launch': "onAppStart"
	    })
	    override_camera_template['nodeGraphOverrides']['nodeOverrides'][0]['with'].append({
	    	'name': '{}'.format(camera)
	    })
    
    # Use targerArn for S3 bucket to download graph.json
    bucket, key = body['targetArn'].split('/',2)[-1].split('/',1)
    print({bucket, key})
    
    
    try:
        s3.meta.client.download_file(bucket, key, '/tmp/graph.json')
        with open("/tmp/graph.json") as graph_json:
	        payload = json.load(graph_json)
	        print(payload)
    except Exception as e:
        # raise e
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Download graph.json fail!!',
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
    
    # Use Comonent_Version_ID for Panorama device id
    try:
        resp = pano_client.create_application_instance(
	    	Name=body['deploymentName'],
	    	ManifestPayload={'PayloadData': json.dumps(payload)},
	    	ManifestOverridesPayload={'PayloadData': json.dumps(override_camera_template)},
	    	DefaultRuntimeContextDevice=body['Component_Version_ID'],
	    	RuntimeRoleArn='arn:aws:iam::201125699002:role/auo_ppe_demo_roles'
	    )
    except Exception as e:
        # raise e
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Panorama Deployment fail!!',
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
    
    
    try:
        response = table.put_item(
            Item={
                'Deployment_ID': body['Deployment_ID'],
                'Device_ID': body['Device_ID'],
                'Camera_ID': body['Camera_ID'],
                'Component_Version_ID': body['Component_Version_ID'],
                'Model_Version_ID': body['Model_Version_ID'],
                'targetArn': body['targetArn'],
                'deploymentName': body['deploymentName'],
                'components': body['components'],
                'deploymentPolicies': body['deploymentPolicies'],
                'iotJobConfigurations': body['iotJobConfigurations']
            }
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': body['Deployment_ID'],
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
    except Exception as e:
        # raise e
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Error!!',
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }


def get(event):
    print(event)
    eprint(">>> Start query config.")

    TABLE_NAME = "PPE_Deployment_table"
    db = boto3.resource('dynamodb')
    table = db.Table(TABLE_NAME)

    try:
        response = table.scan()
        eprint(response)
        eprint(response['ResponseMetadata']['HTTPStatusCode'])
        eprint(response['Items'])
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps(response['Items']),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
    except Exception as e:
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Error!!',
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }


def handler(event, context):
    if event['httpMethod'] == 'POST':
        aws_account_id = context.invoked_function_arn.split(":")[4]
        return post(event, aws_account_id)
    elif event['httpMethod'] == 'GET':
        return get(event)


if __name__ == "__main__":
    pass

