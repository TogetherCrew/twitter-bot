from datetime import datetime, timedelta

from bot.db.latest_tweet import get_latest_tweet_since
from bot.db.neo4j_connection import Neo4jConnection


def test_get_latest_tweet_none():
    """
    test if the latest tweet was `None`
    no data would be inserted
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    id = get_latest_tweet_since(user_id="12345")

    assert id is None


def test_get_latest_tweet():
    """
    test if the latest tweet was not `None`
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    created_time = int((datetime.now() - timedelta(days=2)).timestamp() * 1000)
    neo4j_ops.gds.run_cypher(
        f"""
        MERGE (a:TwitterAccount {{userId: '12345'}})
            -[r:TWEETED]->(t:Tweet {{tweetId: '988776'}})

        SET t.createdAt = {created_time}
        """
    )

    id = get_latest_tweet_since(user_id="12345")

    assert id is not None
    assert id == "988776"
