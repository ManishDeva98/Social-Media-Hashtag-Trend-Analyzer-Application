import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    session = boto3.Session(
        aws_access_key_id='**********************',
        aws_secret_access_key='**************************',
        region_name='eu-north-1'
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('Posts1')
    post_id = event.get('post_id')
    content = event.get('content')
    hashtags = event.get('hashtags')
    timestamp = datetime.utcnow().isoformat()
    
    item = {
        'PostID': post_id,
        'Content': content,
        'Hashtags': hashtags,
        'Timestamp': timestamp
    }  
    '''return {
        'statusCode': 200,
        'body': json.dumps(f'Data successfully written to DynamoDB : {dict(item)}')
    }'''
    try:
        table.put_item(Item=item)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error writing to DynamoDB: {str(e)}')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully written to DynamoDB')
    }
