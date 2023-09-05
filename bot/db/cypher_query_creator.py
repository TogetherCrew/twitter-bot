from datetime import datetime
from typing import Any

from .utils import (  # isort: skip
    create_query,
    relation_query,
    tweet_type_finder,
)

from .enums_data import (  # isort: skip
    EdgeLabels,
    HashtagProperties,
    NodeLabels,
    Properties,
    TweetProperties,
    TwitterAccountProperties,
)


"""
Tweets's structure: {
    tweetId: an unique id for every tweet,
    created_at: creation date of this tweet,
    author_id: this field contains some twitter account id,
    text: text body of tweet,
    image_url: urls for images in this tweet (list),
    video_url: urls for videos in this tweet (list),
    type: showing the type of tweet (quote, reply etc.)
    even using refrenced_tweets for this section,
    hashtags: contains hashtags of this tweet (list),
    account_mentions: contains list of accounts' id
    and username which are mentioned (list),
    likes: shows accounts who are like this tweet (list),
    replies: shows accounts who are reply this tweet (list),
    retweets: shows accounts who are retweet this tweet (list),
    quote_retweets: shows accounts who are like this tweet (list),

    sentiment: (optional)
}


Twitter_accounts' structure: {
    user_id: an unique id for every account,
    username: name this account,
    bio: bio of this account
}
"""


def second_to_datetime(dt):
    ans = str(datetime.fromtimestamp(dt / 1000)) + "+00:00"
    return ans


def create_twitter_data_query(twitter_data: list[dict[str, Any]]) -> list[str]:
    """
    Traverse through the twitter data in order to convert them into
    cypher queries

    Parameters:
    ------------
    twitter_data : list[dict[str, Any]]
        list of tweet dictionary

    Returns:
    ---------
    cypher_queries : list[str]
        the list of cypher queries to run
    """
    # to save the cypher queries
    cypher_queries = []

    j_iter = 0
    for tweet in twitter_data:
        j_iter += 1
        features = []

        # features.append(Properties(TweetProperties.tweet_id, tweet["id"], str))
        features.append(
            Properties(TweetProperties.created_at, tweet["created_at"], datetime)
        )
        features.append(Properties(TweetProperties.author_id, tweet["author_id"], str))
        features.append(Properties(TweetProperties.text, tweet["text"], str))
        features.append(
            Properties(
                TweetProperties.like_counts, tweet["public_metrics"]["like_count"], int
            )
        )
        if "image_url" in tweet.keys() and len(tweet["image_url"]) > 0:
            features.append(
                Properties(TweetProperties.image_url, tweet["image_url"], list)
            )
        if "video_url" in tweet.keys() and len(tweet["video_url"]) > 0:
            features.append(
                Properties(TweetProperties.video_url, tweet["video_url"], list)
            )

        query = create_query(
            NodeLabels.tweet,
            Properties(TweetProperties.tweet_id, tweet["id"], str),
            features,
        )
        cypher_queries.append(query)

        if "author_bio" in tweet.keys():
            query = create_query(
                NodeLabels.twitter_account,
                Properties(TwitterAccountProperties.user_id, tweet["author_id"], str),
                [Properties(TwitterAccountProperties.bio, tweet["author_bio"], str)],
            )
            cypher_queries.append(query)

        query = relation_query(
            NodeLabels.twitter_account,
            NodeLabels.tweet,
            Properties(TwitterAccountProperties.user_id, tweet["author_id"], str),
            Properties(TweetProperties.tweet_id, tweet["id"], str),
            EdgeLabels.tweeted,
            [Properties(TweetProperties.created_at, tweet["created_at"], datetime)],
        )
        cypher_queries.append(query)

        if "hashtags" in tweet.keys():
            # Hashtag section
            for h in tweet["hashtags"]:
                query = create_query(
                    NodeLabels.hashtag,
                    Properties(HashtagProperties.hashtag, h, str),
                    [],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.tweet,
                    NodeLabels.hashtag,
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    Properties(HashtagProperties.hashtag, h, str),
                    EdgeLabels.hashtagged,
                    [
                        Properties(
                            TweetProperties.created_at, tweet["created_at"], datetime
                        )
                    ],
                )
                cypher_queries.append(query)

        if "account_mentions" in tweet.keys():
            # Mention section
            for m in tweet["account_mentions"]:
                query = create_query(
                    NodeLabels.twitter_account,
                    Properties(TwitterAccountProperties.user_id, m["id"], str),
                    [
                        Properties(
                            TwitterAccountProperties.user_name, m["username"], str
                        )
                    ],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.tweet,
                    NodeLabels.twitter_account,
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    Properties(TwitterAccountProperties.user_id, m["id"], str),
                    EdgeLabels.mentioned,
                    [
                        Properties(
                            TweetProperties.created_at, tweet["created_at"], datetime
                        )
                    ],
                )
                cypher_queries.append(query)

        # Like section
        if "likes" in tweet.keys():
            for like in tweet["likes"]:
                # l_features = []
                # l_features.append(
                #     Properties(
                #         TwitterAccountProperties.user_name, like["username"], str
                #     )
                # )
                query = create_query(
                    NodeLabels.twitter_account,
                    Properties(TwitterAccountProperties.user_id, like["user_id"], str),
                    [
                        Properties(
                            TwitterAccountProperties.user_name, like["username"], str
                        )
                    ],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(TwitterAccountProperties.user_id, like["user_id"], str),
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    relation_name=EdgeLabels.liked,
                    relation_properties=[
                        Properties("", "", list)
                    ],  # BUG: no createdAt in available data for relation_properties
                )
                cypher_queries.append(query)

        # Reply section
        if "replies" in tweet.keys():
            for reply in tweet["replies"]:
                r_features = []
                # r_features.append(
                #     Properties(TweetProperties.tweet_id, reply["id"], str)
                # )
                r_features.append(
                    Properties(TweetProperties.author_id, reply["author_id"], str)
                )
                r_features.append(Properties(TweetProperties.text, reply["text"], str))
                r_features.append(
                    Properties(
                        TweetProperties.created_at,
                        second_to_datetime(reply["created_at"]),
                        datetime,
                    )
                )
                r_features.append(Properties("type", EdgeLabels.replied, str))

                query = create_query(
                    NodeLabels.tweet,
                    Properties(TweetProperties.tweet_id, reply["id"], str),
                    r_features,
                )
                cypher_queries.append(query)

                query = create_query(
                    NodeLabels.twitter_account,
                    Properties(
                        TwitterAccountProperties.user_id, reply["author_id"], str
                    ),
                    [],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(
                        TwitterAccountProperties.user_id, reply["author_id"], str
                    ),
                    Properties(TweetProperties.tweet_id, reply["id"], str),
                    relation_name=EdgeLabels.tweeted,
                    relation_properties=[
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(reply["created_at"]),
                            datetime,
                        )
                    ],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.tweet,
                    NodeLabels.tweet,
                    Properties(TweetProperties.tweet_id, reply["id"], str),
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    relation_name=EdgeLabels.replied,
                    relation_properties=[
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(reply["created_at"]),
                            datetime,
                        ),
                    ],
                )
                cypher_queries.append(query)

        # Retweet section
        if "retweets" in tweet.keys():
            for ret in tweet["retweets"]:
                ret_features = []
                ret_features.append(
                    Properties(TwitterAccountProperties.user_name, ret["username"], str)
                )
                ret_features.append(Properties("type", EdgeLabels.retweeted, str))
                query = create_query(
                    NodeLabels.twitter_account,
                    Properties(TwitterAccountProperties.user_id, ret["user_id"], str),
                    ret_features,
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(TwitterAccountProperties.user_id, ret["user_id"], str),
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    relation_name=EdgeLabels.retweeted,
                    relation_properties=[
                        Properties("", "", list)
                    ],  # BUG: no createdAt in available data for relation_properties
                )
                cypher_queries.append(query)

        # Quote section
        if "quote_retweets" in tweet.keys():
            for quote in tweet["quote_retweets"]:
                q_features = []
                q_features.append(
                    Properties(TweetProperties.author_id, quote["author_id"], str)
                )
                q_features.append(Properties(TweetProperties.text, quote["text"], str))
                q_features.append(Properties("type", EdgeLabels.quoted, str))
                q_features.append(
                    Properties(
                        TweetProperties.created_at,
                        second_to_datetime(quote["created_at"]),
                        datetime,
                    )
                )
                query = create_query(
                    NodeLabels.tweet,
                    Properties(TweetProperties.tweet_id, quote["id"], str),
                    q_features,
                )
                cypher_queries.append(query)

                query = create_query(
                    NodeLabels.twitter_account,
                    Properties(
                        TwitterAccountProperties.user_id,
                        quote["author_id"],
                        str,
                    ),
                    [],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(
                        TwitterAccountProperties.user_id, quote["author_id"], str
                    ),
                    Properties(TweetProperties.tweet_id, quote["id"], str),
                    EdgeLabels.tweeted,
                    [
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(quote["created_at"]),
                            datetime,
                        )
                    ],
                )
                cypher_queries.append(query)

                query = relation_query(
                    NodeLabels.tweet,
                    NodeLabels.tweet,
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    Properties(TweetProperties.tweet_id, quote["id"], str),
                    EdgeLabels.quoted,
                    [
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(quote["created_at"]),
                            datetime,
                        )
                    ],
                )
                cypher_queries.append(query)

        # Check is it exist or not
        if tweet["referenced_tweets"] is not None:
            for referenced_tweet in tweet["referenced_tweets"]:
                id_val, type_val = tweet_type_finder(referenced_tweet.data)
                query = relation_query(
                    NodeLabels.tweet,
                    NodeLabels.tweet,
                    Properties(TweetProperties.tweet_id, tweet["id"], str),
                    Properties(TweetProperties.tweet_id, id_val, str),
                    relation_name=type_val,
                    relation_properties=[
                        Properties(
                            TweetProperties.created_at, tweet["created_at"], datetime
                        )
                    ],
                )
                cypher_queries.append(query)

    return cypher_queries
