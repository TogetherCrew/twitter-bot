from datetime import datetime
from typing import Any

# fmt: off
from .utils import (create_query, relation_query, tweet_type_finder,
                   update_query)

# fmt: on

from query_creator.enums_data import (  # isort: skip
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
    hashtags = set()  # for avoinding duplicate hashtags
    accounts = set()  # for avoiding duplicate accounts
    tweets = set()

    # to save the cypher queries
    cypher_queries = []

    j_iter = 0
    for tweet in twitter_data:
        j_iter += 1
        features = []

        features.append(Properties(TweetProperties.tweet_id, tweet["tweet_id"], str))
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
        if len(tweet["image_url"]) > 0:
            features.append(
                Properties(TweetProperties.image_url, tweet["image_url"], list)
            )
        if len(tweet["video_url"]) > 0:
            features.append(
                Properties(TweetProperties.video_url, tweet["video_url"], list)
            )

        if str(tweet["tweet_id"]) in tweets:
            query = update_query(
                NodeLabels.tweet,
                Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
                features,
            )
            cypher_queries.append(query)
        else:
            query = create_query(NodeLabels.tweet, features)
            tweets.add(str(tweet["tweet_id"]))
            cypher_queries.append(query)

        if str(tweet["author_id"]) in accounts:
            query = update_query(
                NodeLabels.twitter_account,
                Properties(TwitterAccountProperties.user_id, tweet["author_id"], str),
                [Properties(TwitterAccountProperties.bio, tweet["author_bio"], str)],
            )
            cypher_queries.append(query)
        else:
            acc_features = []
            acc_features.append(
                Properties(TwitterAccountProperties.user_id, tweet["author_id"], str)
            )
            acc_features.append(
                Properties(TwitterAccountProperties.bio, tweet["author_bio"], str)
            )
            query = create_query(NodeLabels.twitter_account, acc_features)
            cypher_queries.append(query)
            accounts.add(str(tweet["author_id"]))

        query = relation_query(
            NodeLabels.twitter_account,
            NodeLabels.tweet,
            Properties(TwitterAccountProperties.user_id, tweet["author_id"], str),
            Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
            EdgeLabels.tweeted,
            [Properties(TweetProperties.created_at, tweet["created_at"], datetime)],
        )
        cypher_queries.append(query)

        # Hashtag section
        for h in tweet["hashtags"]:
            if h not in hashtags:
                query = create_query(
                    NodeLabels.hashtag, [Properties(HashtagProperties.hashtag, h, str)]
                )
                hashtags.add(h)
            cypher_queries.append(query)

            query = relation_query(
                NodeLabels.tweet,
                NodeLabels.hashtag,
                Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
                Properties(HashtagProperties.hashtag, h, str),
                EdgeLabels.hashtagged,
                [Properties(TweetProperties.created_at, tweet["created_at"], datetime)],
            )
            cypher_queries.append(query)

        # Mention section
        for m in tweet["account_mentions"]:
            m_features = []
            if str(m["id"]) in accounts:
                m_features.append(
                    Properties(TwitterAccountProperties.user_name, m["username"], str)
                )
                query = update_query(
                    NodeLabels.twitter_account,
                    Properties(TwitterAccountProperties.user_id, m["id"], str),
                    m_features,
                )
                cypher_queries.append(query)
            else:
                m_features.append(
                    Properties(TwitterAccountProperties.user_id, m["id"], str)
                )
                m_features.append(
                    Properties(TwitterAccountProperties.user_name, m["username"], str)
                )
                query = create_query(NodeLabels.twitter_account, m_features)
                cypher_queries.append(query)
                accounts.add(str(m["id"]))
            query = relation_query(
                NodeLabels.tweet,
                NodeLabels.twitter_account,
                Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
                Properties(TwitterAccountProperties.user_id, m["id"], str),
                EdgeLabels.mentioned,
                [Properties(TweetProperties.created_at, tweet["created_at"], datetime)],
            )
            cypher_queries.append(query)

        # Like section
        if "likes" in tweet.keys():
            for like in tweet["likes"]:
                l_features = []
                if str(like["user_id"]) in accounts:
                    l_features.append(
                        Properties(
                            TwitterAccountProperties.user_name, like["username"], str
                        )
                    )
                    query = update_query(
                        NodeLabels.twitter_account,
                        Properties(
                            TwitterAccountProperties.user_id, like["user_id"], str
                        ),
                        l_features,
                    )
                    cypher_queries.append(query)

                else:
                    l_features.append(
                        Properties(
                            TwitterAccountProperties.user_name, like["username"], str
                        )
                    )
                    l_features.append(
                        Properties(
                            TwitterAccountProperties.user_id, like["user_id"], str
                        )
                    )
                    query = create_query(NodeLabels.twitter_account, l_features)
                    cypher_queries.append(query)
                    accounts.add(str(like["user_id"]))

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(TwitterAccountProperties.user_id, like["user_id"], str),
                    Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
                    relation_name=EdgeLabels.liked,
                    relation_properties=None,  # BUG: where's the createdAt?
                )
                cypher_queries.append(query)

        # Reply section
        if "replies" in tweet.keys():
            for reply in tweet["replies"]:
                r_features = []
                if str(reply["id"]) not in tweets:
                    r_features.append(
                        Properties(TweetProperties.tweet_id, reply["id"], str)
                    )
                    r_features.append(
                        Properties(TweetProperties.author_id, reply["author_id"], str)
                    )
                    r_features.append(
                        Properties(TweetProperties.text, reply["text"], str)
                    )
                    r_features.append(
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(reply["created_at"]),
                            datetime,
                        )
                    )
                    r_features.append(Properties("type", EdgeLabels.replied, str))

                    query = create_query(NodeLabels.tweet, r_features)
                    cypher_queries.append(query)
                    tweets.add(str(reply["id"]))

                if str(reply["author_id"]) not in accounts:
                    tmp_f = []
                    tmp_f.append(
                        Properties(
                            TwitterAccountProperties.user_id, reply["author_id"], str
                        )
                    )
                    query = create_query(NodeLabels.twitter_account, tmp_f)
                    cypher_queries.append(query)
                    accounts.add(str(reply["author_id"]))

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
                    Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
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
                if str(ret["user_id"]) not in accounts:
                    ret_features.append(
                        Properties(
                            TwitterAccountProperties.user_id, ret["user_id"], str
                        )
                    )
                    ret_features.append(
                        Properties(
                            TwitterAccountProperties.user_name, ret["username"], str
                        )
                    )
                    ret_features.append(Properties("type", EdgeLabels.retweeted, str))
                    query = create_query(NodeLabels.twitter_account, ret_features)
                    cypher_queries.append(query)
                    accounts.add(str(ret["user_id"]))

                query = relation_query(
                    NodeLabels.twitter_account,
                    NodeLabels.tweet,
                    Properties(TwitterAccountProperties.user_id, ret["user_id"], str),
                    Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
                    relation_name=EdgeLabels.retweeted,
                    relation_properties=None,  # BUG: Where's the createdAt?
                )
                cypher_queries.append(query)

        # Quote section
        if "quote_retweets" in tweet.keys():
            for quote in tweet["quote_retweets"]:
                q_features = []
                if str(quote["id"]) not in tweets:
                    q_features.append(
                        Properties(TweetProperties.tweet_id, quote["id"], str)
                    )
                    q_features.append(
                        Properties(TweetProperties.author_id, quote["author_id"], str)
                    )
                    q_features.append(
                        Properties(TweetProperties.text, quote["text"], str)
                    )
                    q_features.append(Properties("type", EdgeLabels.quoted, str))
                    q_features.append(
                        Properties(
                            TweetProperties.created_at,
                            second_to_datetime(quote["created_at"]),
                            datetime,
                        )
                    )
                    query = create_query(NodeLabels.tweet, q_features)
                    cypher_queries.append(query)
                    tweets.add(str(quote["id"]))

                if str(quote["author_id"]) not in accounts:
                    query = create_query(
                        NodeLabels.twitter_account,
                        [
                            Properties(
                                TwitterAccountProperties.user_id,
                                quote["author_id"],
                                str,
                            )
                        ],
                    )
                    accounts.add(str(quote["author_id"]))
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
                    Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
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
            id_val, type_val = tweet_type_finder(tweet["referenced_tweets"])
            query = relation_query(
                NodeLabels.tweet,
                NodeLabels.tweet,
                Properties(TweetProperties.tweet_id, tweet["tweet_id"], str),
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
