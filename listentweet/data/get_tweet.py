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


class TwitterSubjectStreamer(tweepy.StreamListener):
    pass
