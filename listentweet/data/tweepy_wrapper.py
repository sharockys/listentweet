import tweepy
import pandas as pd
from typing import List
from dataclasses import make_dataclass
from listentweet.utils.setup_tweepy import init_tweepy_api
import json
import logging
import time
from pymongo import MongoClient


class TwitterSearcher:
    def __init__(self):
        self.api = init_tweepy_api()

    def retrieve_tweets_by_request(
        self, req: str, n_tweets: int = 10, to_df: bool = False
    ) -> List[str]:
        SimpleTweet = make_dataclass(
            "SimpleTweet",
            [("id", int), ("lang", str), ("text", str), ("created_at", str)],
        )
        results = []
        for tweet in tweepy.Cursor(self.api.search, q=req).items(n_tweets):
            curr_tweet = SimpleTweet(
                tweet.id, tweet.lang, tweet.text, tweet.create_at.ctime()
            )
            results.append(curr_tweet)
        if to_df:
            results = pd.Dataframe(results)
        return results


class TwitterToDBStreamer:
    def __init__(self) -> None:
        self.api = init_tweepy_api()
        self.listener = StreamListenerToDB(api=self.api)
        self.logger = logging.getLogger(__name__)
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)

    def __call__(self, keywords, languages) -> None:
        self._listen(keywords, languages)

    def _listen(self, keywords, languages) -> None:
        self.logger.info(f"starting streaming on {keywords}")
        self.stream.filter(track=keywords, languages=languages, is_async=True)
        while True:
            if not self.stream.running:
                self.logger.error("stream error occured, reset streamer")
                time.sleep(5)
                self.stream = tweepy.Stream(
                    auth=self.api.auth, listener=self.listener
                )
                self.stream.filter(
                    track=keywords, languages=languages, is_async=True
                )


class StreamListenerToDB(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.count = 0
        self.logger = logging.getLogger(__name__)
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client.twitter

    def on_status(self, status):
        self.db.twitter_lines.insert_one(status._json)
        self.count += 1
        print(status)
        self.logger.info(f"Streaming... saved {self.count} tweets to MongoDB.")

    def on_error(self, status_code):
        self.logger.error(f"Error occured with Status Code {status_code}")
        return super().on_error(status_code)


class TwitterToJsonStreamer:
    def __init__(self, filename) -> None:
        self.api = init_tweepy_api()
        self.listener = StreamListenerToJson(filename, api=self.api)
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)
        self.logger = logging.getLogger(__name__)

    def __call__(self, keywords, languages) -> None:
        self._listen(keywords, languages)

    def _listen(self, keywords, languages) -> None:
        self.logger.info(f"starting streaming on {keywords}")
        self.stream.filter(track=keywords, languages=languages, is_async=True)
        while True:
            if not self.stream.running:
                self.logger.error("stream error occured, reset streamer")
                time.sleep(5)
                self.stream = tweepy.Stream(
                    auth=self.api.auth, listener=self.listener
                )
                self.stream.filter(
                    track=keywords, languages=languages, is_async=True
                )


class StreamListenerToJson(tweepy.StreamListener):
    def __init__(self, filename, api):
        self.api = api
        self.fhandler = open(filename, "a+")
        self.count = 0
        self.logger = logging.getLogger(__name__)

    def on_status(self, status):
        json.dump(status._json, self.fhandler)
        self.fhandler.write("\n")
        self.count += 1
        print(status)
        self.logger.info(f"Streaming... saved {self.count} tweets.")

    def on_error(self, status_code):
        self.logger.error(f"Error occured with Status Code {status_code}")
        return super().on_error(status_code)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    stdb = TwitterToDBStreamer()
    keywords = [
        "#laposte",
        "#colissimo",
        "#dpd",
        "#chronopost",
        "Laposte",
        "Colissimo",
        "dpd",
        "chronopost",
    ]
    languages = ["fr", "zh"]
    stdb(keywords, languages)
    # stdb("china", languages)
