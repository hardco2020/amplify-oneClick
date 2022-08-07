import json
import boto3

import sys

# Hack to print to stderr so it appears in CloudWatch.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, ** kwargs)


def post(event):
    print(event)
    TABLE_NAME = "Device-test"
    db = boto3.resource('dynamodb')
    table = db.Table(TABLE_NAME)
    body = json.loads(event['body'])

    print(body['device_id'])
    print(body['device_name'])
    print(body['device_core_name'])
    print(body['core_arn'])
    print(body['type'])
    print(body['use_gpu'])
    print(body['storage'])

    try:
        response = table.put_item(
            Item={
                'device_id': body['device_id'],
                'device_name': body['device_name'],
                'device_core_name': body['device_core_name'],
                'core_arn': body['core_arn'],
                'type': body['type'],
                'use_gpu': body['use_gpu'],
                'storage': body['storage'],
            }
        )
        eprint('OK !!')
        eprint(response)
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': body['device_id'],
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

    TABLE_NAME = "Device-test"
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


if __name__ == "__main__":
    pass
