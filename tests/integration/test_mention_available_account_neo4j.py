from bot.db.neo4j_connection import Neo4jConnection
from bot.db.twitter_data_to_cypher import create_twitter_data_query
from tweepy import Tweet


def test_mention_available_account_neo4j():
    """
    test users being mentioned but was created before
    so a query would be created to set values to them

    We're making a sample data that the user mention themselves
    """
    sample_data = {
        "id": "556644",
        "edit_history_tweet_ids": ["556644"],
        "created_at": "2023-04-14T20:56:58.00Z",
        "author_id": "123456",
        "author_bio": "amazing!",
        "conversation_id": "556644",
        "text": "SAMPLE_TEXT",
        "image_url": [],
        "video_url": [],
        "text_url": [],
        "type": [],
        "hashtags": [],
        "entities": {"mentions": [{"username": "special_user", "id": "123456"}]},
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 0,
            "reply_count": 0,
            "like_count": 0,
            "quote_count": 0,
            "impression_count": 0,
        },
        "context_annotations": [],
        "referenced_tweets": None,
    }
    data = Tweet(data=sample_data)
    queries = create_twitter_data_query([data])

    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    neo4j_ops.store_data_neo4j(queries, message="test_mention_available_account")

    tweet_results = neo4j_ops.gds.run_cypher(
        """
        MATCH (t:Tweet)
        RETURN
        t{.*} as tweet
        """
    )
    assert len(tweet_results) == 1
    data = tweet_results["tweet"].values[0]

    assert data["tweetId"] == "556644"
    assert data["text"] == "SAMPLE_TEXT"
    assert data["authorId"] == "123456"
    assert data["createdAt"] == 1681505818000

    mentioned_results = neo4j_ops.gds.run_cypher(
        """
        MATCH (:Tweet) -[r:MENTIONED] ->()
        RETURN
        r{.*} as mention
        """
    )

    assert len(mentioned_results) == 1
    data = mentioned_results["mention"].values[0]
    assert data["createdAt"] == 1681505818000

    user_results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN
        a{.*} as user
        """
    )
    assert len(user_results) == 1
    data = user_results["user"].values[0]
    print(data)
    # assert data["createdAt"] == 1681505818000
    assert data["userName"] == "special_user"
    assert data["userId"] == "123456"
    assert data["bio"] == "amazing!"
