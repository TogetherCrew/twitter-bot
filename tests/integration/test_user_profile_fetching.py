from bot.db.neo4j_connection import Neo4jConnection
from datetime import datetime

from bot.db.user_profile_to_cypher import create_twitter_user_profile_query

from tweepy import User


def test_user_profile_saving():
    """
    save
    """
    user_data = {
        "url": "https://t.co/ui89pZjLNx",
        "username": "katerinabohlec",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1033847263397912576/9okABKa5_normal.jpg",
        "id": "2220997760",
        "description": "Scientist 👩\u200d🏫 | Writer | Explorer @RnDAO__ @together_crew 📆 https://t.co/m2abdcGZ0D 👩\u200d👧\u200d👧4x mum https://t.co/zIJ2lSbKu2",
        "verified": False,
        "name": "Katerina (💫,💫) 🚂 MetaFest",
        "location": "⛺️🌎",
        "protected": False,
        "created_at": "2013-11-29T07:10:24.000Z"
        # 'created_at': datetime.strptime(
        #     '2013-11-29 07:10:24+00:00',
        #     "%Y-%m-%d %H:%M:%S%z"
        # )
    }
    sample_user = User(data=user_data)

    queries = create_twitter_user_profile_query([sample_user])

    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    neo4j_ops.store_data_neo4j(query_list=queries)

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
