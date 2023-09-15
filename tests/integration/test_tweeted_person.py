from bot.db.neo4j_connection import Neo4jConnection
from bot.db.twitter_data_to_cypher import create_twitter_data_query
from tweepy import Tweet


def test_create_tweeted_person_neo4j():
    """
    create queries for a person that tweets a tweet (relationships included)
    """
    sample_data = {
        "id": "223344",
        "edit_history_tweet_ids": ["223344"],
        "created_at": "2023-04-13T01:21:51.00Z",
        "author_id": "12344321",
        "author_bio": "Amazing man with a perfect profile!",
        "conversation_id": "223344",
        "text": "IYKYK - @user2 https://somelink",
        "image_url": ["https://twitter.com/amazingman/status/223344/photo/1"],
        "video_url": ["https://twitter.com/amazingman/status/223344/video/1"],
        "text_url": [],
        "type": [],
        "hashtags": [],
        "entities": {"mentions": [{"username": "user2", "id": "987789"}]},
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 1,
            "reply_count": 0,
            "like_count": 5,
            "quote_count": 0,
            "impression_count": 415,
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
    neo4j_ops.store_data_neo4j(queries, message="test_create_tweeted_person_neo4j")

    results_tweet = neo4j_ops.gds.run_cypher(
        """
        MATCH (t:Tweet)
        RETURN t{.*} as tweet
        """
    )
    assert len(results_tweet) == 1
    data = results_tweet["tweet"].values[0]
    assert data["createdAt"] == 1681348911000
    assert data["text"] == "IYKYK - @user2 https://somelink"
    assert data["authorId"] == "12344321"
    assert data["likeCounts"] == 5
    assert data["imageUrl"] == ["https://twitter.com/amazingman/status/223344/photo/1"]
    assert data["videoUrl"] == ["https://twitter.com/amazingman/status/223344/video/1"]

    results_account = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN a{.*} as account
        """
    )
    assert len(results_account) == 2

    for _, row in results_account.iterrows():
        data = row["account"]
        assert data["userId"] in ["12344321", "987789"]
        if data["userId"] == "12344321":
            assert "userName" not in data
            assert data["bio"] == "Amazing man with a perfect profile!"
        else:
            assert data["userName"] == "user2"
            assert data["userId"] == "987789"
            assert "bio" not in data

    results_tweeted_rel = neo4j_ops.gds.run_cypher(
        """
        MATCH ()-[r:TWEETED]->()
        RETURN r{.*} as tweeted_rel
        """
    )
    assert len(results_tweeted_rel) == 1
    data = results_tweeted_rel["tweeted_rel"].values[0]
    assert data["createdAt"] == 1681348911000

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:Tweet)-[r:MENTIONED]->(b:TwitterAccount)
        RETURN
            r{.*} as mentioned,
            a{.*} as tweet,
            b{.*} as account
        """
    )
    assert len(results) == 1
    data = results["mentioned"].values[0]
    assert data["createdAt"] == 1681348911000

    data = results["tweet"].values[0]
    assert data["tweetId"] == "223344"
    assert data["authorId"] == "12344321"

    data = results["account"].values[0]
    assert data["userId"] == "987789"
    assert data["userName"] == "user2"
