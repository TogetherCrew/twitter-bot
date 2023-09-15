from bot.db.latest_tweet import get_days_ago_tweet_ids
from bot.db.neo4j_connection import Neo4jConnection
from bot.db.save_neo4j import save_tweets_in_neo4j
from tweepy import Tweet


def test_get_days_ago_tweet_ids_none_data():
    """
    get the tweetIDs of past 7 days in case of no data available
    results should be an empty array
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    ids = get_days_ago_tweet_ids(user_id="1111")
    assert ids == []


def test_get_days_ago_tweet_ids_with_all_tweets_past_days():
    """
    get the data for past 7 days in case of having some data
    all tweets within the past 7 days
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    sample_data = [
        {
            "entities": {
                "annotations": [
                    {
                        "start": 16,
                        "end": 24,
                        "probability": 0.6081,
                        "type": "Other",
                        "normalized_text": "Wellbeing",
                    }
                ],
                "hashtags": [
                    {"start": 15, "end": 25, "tag": "Wellbeing"},
                    {"start": 26, "end": 36, "tag": "happylife"},
                ],
            },
            "public_metrics": {
                "retweet_count": 0,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 2,
            },
            "id": "12345",
            "text": "sample hastags #Wellbeing #happylife",
            "edit_history_tweet_ids": ["12345"],
            "conversation_id": "12345",
            "created_at": "2023-09-07T13:09:52.000Z",
            "author_id": "11111",
        },
        {
            "entities": {
                "urls": [
                    {
                        "start": 14,
                        "end": 37,
                        "url": "https://t.co/somelink",
                        "expanded_url": "http://somelink.com/",
                        "display_url": "somelink.com",
                        "status": 200,
                        "title": "Google",
                        "description": "some description",
                        "unwound_url": "http://www.somelink.com/",
                    }
                ]
            },
            "public_metrics": {
                "retweet_count": 0,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 1,
            },
            "id": "12346",
            "text": "Posting a url https://t.co/somelink",
            "edit_history_tweet_ids": ["12346"],
            "conversation_id": "12346",
            "created_at": "2023-09-07T12:32:00.000Z",
            "author_id": "11111",
        },
        {
            "public_metrics": {
                "retweet_count": 0,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 1,
            },
            "context_annotations": [
                {
                    "domain": {
                        "id": "47",
                        "name": "Brand",
                        "description": "Brands and Companies",
                    },
                    "entity": {"id": "10045225402", "name": "Twitter"},
                }
            ],
            "id": "12347",
            "text": "Another tweet!",
            "edit_history_tweet_ids": ["12347"],
            "conversation_id": "12347",
            "created_at": "2023-09-07T12:29:07.000Z",
            "author_id": "11111",
        },
        {
            "public_metrics": {
                "retweet_count": 0,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "bookmark_count": 0,
                "impression_count": 2,
            },
            "id": "12348",
            "text": "mentioning someone in case of something @person",
            "edit_history_tweet_ids": ["12348"],
            "conversation_id": "12348",
            "created_at": "2023-09-07T12:09:25.000Z",
            "entities": {
                "mentions": [
                    {
                        "start": 40,
                        "end": 49,
                        "username": "person",
                        "id": "11112",
                    }
                ]
            },
            "author_id": "11111",
        },
    ]
    tweets_data: list[Tweet] = []
    for data in sample_data:
        tweet = Tweet(data=data)
        tweets_data.append(tweet)

    save_tweets_in_neo4j(tweets_data, message="test_get_days_ago_tweet_ids_with_data")

    ids = get_days_ago_tweet_ids(user_id="11111")

    assert ids == [
        "12345",
        "12346",
        "12347",
        "12348",
    ]
