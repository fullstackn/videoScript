import os
import tweepy

from common import get_full_caption

client_id = os.environ.get('TWITTER_CLIENT_ID')
client_secret = os.environ.get('TWITTER_CLIENT_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
api_key = os.environ.get('TWITTER_API_KEY')
api_secret = os.environ.get('TWITTER_API_SECRET')


def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)


def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client


def upload_tweet(video_path, title, caption, tags):
    # initiate two clients (we need different ones for uploading media and for posting)
    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
    media = client_v1.media_upload(filename=video_path)
    text = get_full_caption(title, caption, tags)
    client_v2.create_tweet(text=text, media_ids=[media.media_id])