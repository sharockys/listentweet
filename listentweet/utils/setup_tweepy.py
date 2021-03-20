import dotenv
import os
import tweepy
from listentweet.settings import *


def get_auth_dotenv():
    dotenv_path = os.path.join(PROJECT_DIR, ".env")
    dotenv.load_dotenv(dotenv_path)
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    return api_key, api_secret, access_token, access_token_secret


def init_tweepy_api():
    api_key, api_secret, access_token, access_token_secret = get_auth_dotenv()
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api
