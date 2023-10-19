from datetime import datetime, timedelta

from bot.db.latest_reply import get_latest_reply_since
from bot.db.neo4j_connection import Neo4jConnection


def test_get_latest_reply_userid_input_output_none():
    """
    get the latest tweetId base on given user_id
    the output should be `None`
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    id = get_latest_reply_since(user_id="12345")

    assert id is None


def test_get_latest_reply_tweetId_input_output_none():
    """
    get the latest tweetId base on given user_id
    the output should be `None`
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    id = get_latest_reply_since(tweet_id="12345")

    assert id is None


def test_get_latest_reply_empty_inputs_output_none():
    """
    show exception message as we didn't give any inputs
    the output should be `None`
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    try:
        _ = get_latest_reply_since(user_id=None, tweet_id=None)
    except ValueError as exp:
        assert str(exp) == "`tweet_id` and `user_id` are both None!"


def test_get_latest_reply_userid_input():
    """
    get the latest tweetId base on given user_id
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
        MERGE (a:Tweet {{tweetId: '1111', authorId: '989898'}})
        MERGE (b:Tweet {{tweetId: '1112', authorId: '989899'}})
        MERGE (c:Tweet {{tweetId: '1113', authorId: '9898100'}})
        MERGE (d:Tweet {{tweetId: '1114', authorId: '989898'}})
        MERGE (e:Tweet {{tweetId: '1115', authorId: '989897'}})

        MERGE (a)-[r:REPLIED]->(b)
        MERGE (d)-[r2:REPLIED]->(a)
        MERGE (e)-[r3:REPLIED]->(a)
        MERGE (d)-[r4:REPLIED]->(b)
        MERGE (c)-[r5:REPLIED]->(d)


        SET r.createdAt = {created_time}
        SET r2.createdAt = {created_time}
        SET r3.createdAt = {created_time}
        SET r4.createdAt = {created_time}
        SET r5.createdAt = {created_time}
        """
    )

    id = get_latest_reply_since(user_id="989898")

    assert id is not None
    assert id == "1115"


def test_get_latest_reply_tweetid_input():
    """
    get the latest tweetId base on given `tweetid`
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
        MERGE (a:Tweet {{tweetId: '1111', authorId: '989898'}})
        MERGE (b:Tweet {{tweetId: '1112', authorId: '989899'}})
        MERGE (c:Tweet {{tweetId: '1113', authorId: '9898100'}})
        MERGE (d:Tweet {{tweetId: '1114', authorId: '989898'}})
        MERGE (e:Tweet {{tweetId: '1115', authorId: '989897'}})

        MERGE (a)-[r:REPLIED]->(b)
        MERGE (c)-[r2:REPLIED]->(a)
        MERGE (d)-[r3:REPLIED]->(a)
        MERGE (e)-[r4:REPLIED]->(a)
        MERGE (c)-[r5:REPLIED]->(d)

        SET r.createdAt = {created_time}
        SET r2.createdAt = {created_time}
        SET r3.createdAt = {created_time}
        SET r4.createdAt = {created_time}
        SET r5.createdAt = {created_time}
        """
    )

    id = get_latest_reply_since(tweet_id="1111")

    assert id is not None
    assert id == "1115"
