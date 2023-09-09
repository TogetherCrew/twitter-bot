import numpy as np
from tweepy import User

from bot.db.neo4j_connection import Neo4jConnection
from bot.db.save_neo4j import save_tweet_likes_neo4j


def test_tweet_likes_empty_input():
    """
    test the module in case of empty inputs
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    save_tweet_likes_neo4j(tweet_id="1111", users_liked=[])

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (n) RETURN COUNT (n) as data_count
        """
    )

    assert results["data_count"].iloc[0] == 0


def test_likes_single_input():
    """
    test the like of a tweet to be just one user
    """
    user_data = {
        "url": "https://t.co/theurl",
        "username": "sample_user",
        "profile_image_url": "https://person_image",
        "id": "12345",
        "description": "peoplepeoplepeople",
        "verified": False,
        "name": "sample_user_name",
        "location": "Berlin",
        "protected": False,
        "created_at": "2013-11-29T07:10:24.000Z",
        "public_metrics": {
            "followers_count": 0,
            "following_count": 0,
            "tweet_count": 4,
            "listed_count": 0,
        },
    }
    sample_user = User(data=user_data)

    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    save_tweet_likes_neo4j(tweet_id="1111", users_liked=[sample_user])

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount {userId: "12345"})
            -[r:LIKED]->(t:Tweet {tweetId: "1111"})
        RETURN
            a.userId as user_id,
            r.latestSavedAt as relation_timestamp,
            t.tweetId as tweet_id
        """
    )
    print(results)
    assert len(results) == 1
    user_id = results["user_id"].iloc[0]
    relation_time = results["relation_timestamp"].iloc[0]
    tweet_id = results["tweet_id"].iloc[0]

    assert tweet_id == "1111"
    assert user_id == "12345"
    assert isinstance(relation_time, np.int64)


def test_likes_multiple_inputs():
    """
    test the like of a tweet to be multiple users
    """
    users_data = [
        {
            "url": "https://t.co/theurl",
            "username": "sample_user",
            "profile_image_url": "https://person_image",
            "id": "12345",
            "description": "peoplepeoplepeople",
            "verified": False,
            "name": "sample_user_name",
            "location": "Berlin",
            "protected": False,
            "created_at": "2013-11-29T07:10:24.000Z",
            "public_metrics": {
                "followers_count": 0,
                "following_count": 0,
                "tweet_count": 4,
                "listed_count": 0,
            },
        },
        {
            "url": "https://t.co/theurl2",
            "username": "sample_user2",
            "profile_image_url": "https://person_image2",
            "id": "12346",
            "description": "peoplepeoplepeople2",
            "verified": False,
            "name": "sample_user_name2",
            "location": "Berlin2",
            "protected": False,
            "created_at": "2020-11-29T07:10:24.000Z",
            "public_metrics": {
                "followers_count": 1,
                "following_count": 5,
                "tweet_count": 8,
                "listed_count": 12,
            },
        },
    ]
    tweepy_users = []
    for user in users_data:
        sample_user = User(data=user)
        tweepy_users.append(sample_user)
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    save_tweet_likes_neo4j(tweet_id="1111", users_liked=tweepy_users)

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
            -[r:LIKED]->(t:Tweet {tweetId: "1111"})
        RETURN
            a.userId as user_id,
            r.latestSavedAt as relation_timestamp,
            t.tweetId as tweet_id
        """
    )
    print(results)
    assert len(results) == 2
    assert results["user_id"].iloc[0] in ["12345", "12346"]
    assert results["user_id"].iloc[1] in ["12345", "12346"]

    relation_time = results["relation_timestamp"].iloc[0]
    relation_time2 = results["relation_timestamp"].iloc[1]
    assert results["tweet_id"].iloc[0] == "1111"
    assert results["tweet_id"].iloc[1] == "1111"

    assert isinstance(relation_time, np.int64)
    assert isinstance(relation_time2, np.int64)
