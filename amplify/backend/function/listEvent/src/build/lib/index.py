# DB
TABLE_NAME = "PPE_Event_table"
db = boto3.resource('dynamodb')
table = db.Table(TABLE_NAME)

#S3
s3 = boto3.client('s3')
def handler(event, context):
    # TODO implement
    if event['httpMethod'] == 'GET':
        results = {}
        results['data'] = {}
        results['data']['content'] = []
        print(response)
        for item in response['Items']:
            good = {}
            good['name'] = item['payload']['name']
            print(item['payload']['time'])
            good['time'] = item['payload']['time']
            good['location'] = item['payload']['location']
            good['device_id'] = item['payload']['device_id']
            good['picture'] = get_presigned_url(item['payload']['picture'])
            if len(item['payload']['video']) > 0:
                good['video'] = get_presigned_url(item['payload']['video'])
            if len(item['payload']['label']) > 0:
                good['video'] = get_presigned_url(item['payload']['label'])
            #good['label'] = get_presigned_url(item['payload']['label'])
            good['origin_picture'] = get_presigned_url(item['payload']['origin_picture'])
            
            results['data']['content'].append(good)
        body = json.dumps(results)
    # elif event['httpMethod'] == 'POST':
    #     if 'pathParameters' in event:
    #         doc_id = event['pathParameters']['doc_id']
    #         #print(doc_id)
    #         #print(evet['body'])
    #         es.update(
    #             index=es_index,
    #             id=doc_id,
    #             body={
    #                 "doc": json.loads(event['body'])
    #             },
    #             doc_type="_doc"
    #         )
    #     body = ""

    return {
        'statusCode': 200,
        'body': body,
        'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }

def get_presigned_url(s3uri):
    print('got hit')
    print('123')
    first = s3uri.find('/', 5)
    # bucket = bucket=s3uri[5 : first]
    print(s3uri)
    bucket = s3uri[5: first]
    print(bucket)

    file_key = s3uri[first + 1:]
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket, 'Key': file_key},
            ExpiresIn=1000
        )
        print("Got presigned URL: {}".format(url))
    except ClientError:
        print("Couldn't get a presigned URL for client method {}.".format(client_method))
        raise