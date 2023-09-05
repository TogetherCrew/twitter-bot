from neo4j_connection import connect_neo4j
from query_creator.cypher_query_creator import create_twitter_data_query


def test_mention_available_account_neo4j():
    """
    test users being mentioned but was created before
    so a query would be created to set values to them

    We're making a sample data that the user mention themselves
    """
    sample_data = {
        "tweet_id": "000000",
        "created_at": "2023-04-14 20:56:58+00:00",
        "author_id": "123456",
        "author_bio": "amazing!",
        "conversation_id": "000000",
        "text": "SAMPLE_TEXT",
        "image_url": [],
        "video_url": [],
        "text_url": [],
        "type": [],
        "hashtags": [],
        "account_mentions": [{"username": "special_user", "id": "123456"}],
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

    queries = create_twitter_data_query([sample_data])

    neo4j_ops = connect_neo4j()

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

    assert data["tweetId"] == "000000"
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
