import tweepy
import pandas as pd
from typing import List
from dataclasses import make_dataclass
from listentweet.utils.setup_tweepy import init_tweepy_api


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


class StreamTwitterToDB:
    def __init__(self) -> None:
        self.api = init_tweepy_api()
        self.listener = tweepy.StreamListenerToDB()
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)

    def __call__(self, keyword) -> None:
        self.stream.filter(track=[keyword])


# Todo: Add DB settings
class StreamListenerToDB:
    def on_status(self, status):
        pass
