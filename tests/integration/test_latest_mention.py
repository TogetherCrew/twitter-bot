from bot.db.latest_mention import get_latest_mention_in_past_7_days
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

    id = get_latest_mention_in_past_7_days(user_id="12345")

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

    neo4j_ops.gds.run_cypher(
        """
        MERGE (:Tweet {tweetId: '00000', authorId: '989898'})
            -[:MENTIONED]->(a:TwitterAccount {userId: '11111'})
        """
    )

    id = get_latest_mention_in_past_7_days(user_id="11111")

    assert id is not None
    assert id == "00000"
