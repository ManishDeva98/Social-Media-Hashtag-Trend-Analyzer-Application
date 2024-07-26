import streamlit as st
import boto3
import uuid
import json
import time
from boto3.dynamodb.conditions import Attr
import requests

# Set up Boto3 client for Lambda


# Function to invoke Lambda
def post_to_lambda(post_content, hashtags):
    session = boto3.Session(
        aws_access_key_id='AKIA***********S',
        aws_secret_access_key='Hi5K*******************8kEK78xU',
        region_name='eu-north-1'
    )
    lambda_client = session.client('lambda')
    post_id = str(uuid.uuid4())
    payload = {
        'post_id': post_id,
        'content': post_content,
        'hashtags': hashtags
    }
    response = lambda_client.invoke(
        FunctionName='HashtagTrend',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.loads(response['Payload'].read())

# Function to get trending hashtags
def get_trending_hashtags():
    session = boto3.Session(
        aws_access_key_id='AKIA**************S',
        aws_secret_access_key='Hi5K**********************8kEK78xU',
        region_name='eu-north-1'
    )
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('Posts')
    
    response = table.scan()
    items = response['Items']
    
    hashtag_count = {}
    for item in items:
        hashtags = item.get('hashtags', [])
        for hashtag in hashtags:
            if hashtag in hashtag_count:
                hashtag_count[hashtag] += 1
            else:
                hashtag_count[hashtag] = 1
                
    sorted_hashtags = sorted(hashtag_count.items(), key=lambda x: x[1], reverse=True)
    trending_hashtags = [hashtag for hashtag, count in sorted_hashtags[:5]]
    
    return trending_hashtags

# Streamlit UI
st.title('Compose and Publish Post')
post_content = st.text_area('Post Content')
hashtags = st.text_input('Hashtags (comma-separated)')

if st.button('Publish'):
    hashtags_list = [tag.strip() for tag in hashtags.split(',')]
    response = post_to_lambda(post_content, hashtags_list)
    st.success('Post published successfully!')

st.header('Trending Hashtags')
trending_hashtags = get_trending_hashtags()
st.write(trending_hashtags)


