import streamlit as st
import boto3
import requests
import json
import time

# Streamlit application to compose and publish posts
st.title('Compose a Post')

post_content = st.text_area("Write your post here...")
hashtags = st.text_input("Add hashtags (comma-separated)")

if st.button('Publish'):
    hashtags_list = hashtags.split(',')
    data = {
        'post_content': post_content,
        'hashtags': hashtags_list
    }
    
    response = requests.post('YOUR_AWS_LAMBDA_ENDPOINT', json=data)
    
    if response.status_code == 200:
        st.success('Post published successfully!')
    else:
        st.error('Failed to publish post.')

# Display trending hashtags
st.title('Trending Hashtags')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Posts')

def get_trending_hashtags():
    response = table.scan()
    items = response['Items']
    hashtags_count = {}
    
    for item in items:
        for hashtag in item['hashtags']:
            if hashtag in hashtags_count:
                hashtags_count[hashtag] += 1
            else:
                hashtags_count[hashtag] = 1
    
    sorted_hashtags = sorted(hashtags_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_hashtags[:10]

while True:
    trending_hashtags = get_trending_hashtags()
    
    for hashtag, count in trending_hashtags:
        st.write(f"{hashtag}: {count} mentions")
    
    time.sleep(60)  # Refresh every 60 seconds
    st.experimental_rerun()