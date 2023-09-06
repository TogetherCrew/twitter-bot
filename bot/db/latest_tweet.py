from .neo4j_connection import Neo4jConnection


def get_latest_tweet(
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
    latest_tweeted_id : str | None
        the latest tweet's tweetId for the specific user
        if no TWEETED relationship was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # latest tweet id as a dataframe
    df_latest_tweeted = gds.run_cypher(
        f"""
        OPTIONAL MATCH (a:TwitterAccount {{userId: '{user_id}'}})-[r:TWEETED]->(m:Tweet)
        WITH MAX(SIZE(m.tweetId)) as max_size, m.tweetId as id
        RETURN MAX(id) as latest_tweeted_id
        """
    )
    latest_tweeted_id = df_latest_tweeted["latest_tweeted_id"].iloc[0]

    return latest_tweeted_id
