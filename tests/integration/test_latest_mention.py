from datetime import datetime, timedelta

from bot.db.latest_mention import get_latest_mention_since
from bot.db.neo4j_connection import Neo4jConnection


def test_get_latest_mention_none():
    """
    we should get the latest mention of the user as `None`
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    id = get_latest_mention_since(user_id="12345")

    assert id is None


def test_get_latest_mention():
    """
    we should get the latest mention of the user
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
        MERGE (:Tweet {{tweetId: '00000', authorId: '989898'}})
            -[r:MENTIONED]->(a:TwitterAccount {{userId: '11111'}})
        SET r.createdAt = {created_time}
        """
    )

    id = get_latest_mention_since(user_id="11111")

    assert id is not None
    assert id == "00000"
