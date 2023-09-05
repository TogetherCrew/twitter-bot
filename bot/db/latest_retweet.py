from .neo4j_connection import Neo4jConnection


def get_latest_retweet(
    user_id: str,
) -> str:
    """
    get the user handle to get their latest retweet's tweetId

    Parameters:
    ------------
    user_id : str | None
        given the userId, find the required information

    Returns:
    ---------
    latest_retweet_id : str | None
        the latest retweet's tweetId for the specific user
        if no retweet was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # latest retweet as a dataframe
    df_latest_retweet = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:RETWEETED]-(m:Tweet)
        WHERE m.authorId <> '{user_id}'
        RETURN toString(MAX(toInteger(m.tweetId))) as latest_retweet_id
        """
    )
    latest_retweet_id = df_latest_retweet["latest_retweet_id"].iloc[0]

    return latest_retweet_id
