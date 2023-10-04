from bot.db.latest_retweet import get_latest_retweet_since
from bot.db.neo4j_connection import Neo4jConnection


def test_get_latest_retweet_userid_input_output_none():
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

    id = get_latest_retweet_since(user_id="12345")

    assert id is None


def test_get_latest_retweet_tweetId_input_output_none():
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

    id = get_latest_retweet_since(tweet_id="12345")

    assert id is None


def test_get_latest_retweet_empty_inputs_output_none():
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
        _ = get_latest_retweet_since(user_id=None, tweet_id=None)
    except ValueError as exp:
        assert str(exp) == "`tweet_id` and `user_id` are both None!"


def test_get_latest_retweet_userid_input():
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

    neo4j_ops.gds.run_cypher(
        """
        MERGE (a:Tweet {tweetId: '1111', authorId: '989898'})
        MERGE (b:Tweet {tweetId: '1112', authorId: '989899'})
        MERGE (c:Tweet {tweetId: '1113', authorId: '9898100'})
        MERGE (d:Tweet {tweetId: '1114', authorId: '989898'})

        MERGE (a)-[:RETWEETED]->(b)
        MERGE (d)-[:RETWEETED]->(a)
        MERGE (d)-[:RETWEETED]->(b)
        MERGE (c)-[:RETWEETED]->(d)
        """
    )

    id = get_latest_retweet_since(user_id="989898")

    assert id is not None
    assert id == "1114"


def test_get_latest_retweet_tweetid_input():
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

    neo4j_ops.gds.run_cypher(
        """
        MERGE (a:Tweet {tweetId: '1111', authorId: '989898'})
        MERGE (b:Tweet {tweetId: '1112', authorId: '989899'})
        MERGE (c:Tweet {tweetId: '1113', authorId: '9898100'})
        MERGE (d:Tweet {tweetId: '1114', authorId: '989898'})

        MERGE (a)-[:RETWEETED]->(b)
        MERGE (c)-[:RETWEETED]->(a)
        MERGE (d)-[:RETWEETED]->(a)
        MERGE (c)-[:RETWEETED]->(d)
        """
    )

    id = get_latest_retweet_since(tweet_id="1111")

    assert id is not None
    assert id == "1114"
