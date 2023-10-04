from bot.utils.get_epoch import get_x_days_ago_UTC_timestamp

from .neo4j_connection import Neo4jConnection


def get_latest_mention_in_past_7_days(
    user_id: str,
) -> str | None:
    """
    get the user handle to get their latest mantion's tweetId

    Parameters:
    ------------
    user_id : str
        given the userId, find the required information

    Returns:
    ---------
    latest_mention_id : str | None
        the latest mention tweetId for the specific user
        if no mention was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds
    seven_days_ago_timestamp = get_x_days_ago_UTC_timestamp(7)

    # latest mantion as a dataframe
    df_latest_mention = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet)
            -[r:MENTIONED]->(a:TwitterAccount {{userId: '{user_id}'}})
        WHERE r.createdAt >= {seven_days_ago_timestamp}
        WITH MAX(SIZE(t.tweetId)) as max_size, t.tweetId as id
        RETURN MAX(id) as latest_mention_id
        """
    )
    latest_mention_id = df_latest_mention["latest_mention_id"].iloc[0]

    return latest_mention_id
