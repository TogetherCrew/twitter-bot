from bot.db.neo4j_connection import Neo4jConnection
from bot.db.save_neo4j import save_user_profile_neo4j
from tweepy import User


def test_user_profile_saving_none_data():
    """
    using our save module
    give no data to the function and it should not produce any results
    """

    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    save_user_profile_neo4j([])

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (n)
        RETURN COUNT(n) as entity_count
        """
    )

    assert results["entity_count"].iloc[0] == 0


def test_user_profile_saving():
    """
    using our save module
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

    save_user_profile_neo4j([sample_user])

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN a{.*} as account_data
        """
    )

    account = results["account_data"].iloc[0]

    print(account)

    assert account["userName"] == user_data["username"]
    assert account["name"] == user_data["name"]
    assert account["userId"] == user_data["id"]
    assert account["location"] == user_data["location"]
    assert account["verified"] == user_data["verified"]
    assert account["bio"] == user_data["description"]
    assert account["url"] == user_data["url"]
    assert account["profileImageUrl"] == user_data["profile_image_url"]
    assert account["followerCount"] == user_data["public_metrics"]["followers_count"]
    assert account["followingCount"] == user_data["public_metrics"]["following_count"]
