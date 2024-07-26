import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    session = boto3.Session(
        aws_access_key_id='AKIA**************S',
        aws_secret_access_key='Hi5K***************U',
        region_name='eu-north-1'
    )

    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('Posts')
    post_id = event['post_id']
    content = event['content']
    hashtags = event['hashtags']
    timestamp = datetime.utcnow().isoformat()
    
    item = {
        'PostID': post_id,
        'Content': content,
        'Hashtags': hashtags,
        'Timestamp': timestamp
    } 
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Post saved successfully!')
    }