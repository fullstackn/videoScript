import base64
import hashlib
import os
import re
import time
import requests
import tweepy
from requests_oauthlib import OAuth2Session
from flask import Flask, redirect, session, request

auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"

client_id = os.environ['TWITTER_CLIENT_ID']
client_secret = os.environ['TWITTER_CLIENT_SECRET']
access_token = os.environ['TWITTER_CLIENT_ACCESS_TOKEN']
access_secret = os.environ['TWITTER_CLIENT_ACCESS_SECRET']
api_key = os.environ['TWITTER_API_KEY']
api_secret = os.environ['TWITTER_API_SECRET']
callback_host = os.environ['TWITTER_CALLBACK_HOST']

redirect_uri = f'https://{callback_host}/oauth/callback'

app = Flask(__name__)
app.secret_key = os.urandom(50)

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

# Create a code challenge
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]


def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)


def post_tweet(text, video_path, token):
    upload_result = api.media_upload(video_path)
    payload = {
        'text': text,
        'media': {'media_ids': [upload_result.media_id_string]}
    }
    r = requests.post(
        url="https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
        },
    )
    return r


@app.route("/")
def demo():
    global twitter
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    response = post_tweet(
        text=f'post tweet {time.time()=} ',
        video_path='vid99.mp4',
        token=token).json()
    return response


if __name__ == "__main__":
    from pyngrok import ngrok
    http_tunnel = ngrok.connect(addr=5000, hostname=callback_host)
    app.run()
