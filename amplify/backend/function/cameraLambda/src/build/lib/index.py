import json
import boto3
import sys


TABLE_NAME = "Camera-test"

# Hack to print to stderr so it appears in CloudWatch.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, ** kwargs)


def post(event):
    print(event)
    return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }
    db = boto3.resource('dynamodb')
    pano_client = boto3.client('panorama')
    table = db.Table(TABLE_NAME)
    body = json.loads(event['body'])
    
    CAMERA_NAME = body['brand']
    CAMERA_CREDS = {
        "Username": body['location'],
        "Password": body['network'],
        "StreamUrl": body['address']
    }

    print(body['camera_id'])
    print(body['address'])
    print(body['description'])
    print(body['location'])
    print(body['brand'])
    print(body['network'])
    print(body['image_size'])
    
    try:
        pano_res = pano_client.create_node_from_template_job(
            NodeName=CAMERA_NAME,
            OutputPackageName=CAMERA_NAME,
            OutputPackageVersion='0.1',
            TemplateParameters=CAMERA_CREDS,
            TemplateType='RTSP_CAMERA_STREAM'
        )
    except Exception as e:
        eprint('Error !!')
        eprint(e)
        

    try:
        response = table.put_item(
            Item={
                'camera_id': body['camera_id'],
                'address': body['address'],
                'description': body['description'],
                'location': body['location'],
                'brand': body['brand'],
                'network': body['network'],
                'image_size': body['image_size'],
                'JobId': pano_res['JobId'],
            }
        )
        eprint('OK !!')
        eprint(response)
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': body['camera_id']
            'headers': {
                 "Access-Control-Allow-Headers" : "*",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
            }
        }
    except Exception as e:
        # raise e
        eprint('Error !!')
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Error!!'
        }


def get(event):
    print(event)
    eprint(">>> Start query config.")
    result = ""
    db = boto3.resource('dynamodb')
    table = db.Table(TABLE_NAME)

    try:
        response = table.scan()
        eprint(response)
        eprint(response['ResponseMetadata']['HTTPStatusCode'])
        eprint(response['Items'])
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps(response['Items'])
            'headers': {
                "Access-Control-Allow-Headers" : "*",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
            }
        }
    except Exception as e:
        eprint(e)
        return {
            'statusCode': 500,
            'body': 'Error!!'
        }


def handler(event, context):
    if event['httpMethod'] == 'POST':
        return post(event)
    elif event['httpMethod'] == 'GET':
        return get(event)
