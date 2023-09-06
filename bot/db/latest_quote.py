from .neo4j_connection import Neo4jConnection


def get_latest_quote(
    user_id: str | None = None, tweet_id: str | None = None
) -> str | None:
    """
    get the user handle to get their latest quote's tweetId
    or using the tweet_id find its latest quote

    Parameters:
    ------------
    user_id : str | None
        given the userId, find the required information
    tweet_id : str | None
        given the tweet_id, find the required information
        should be either `user_id` or `tweet_id` be given
        if both was given tweet_id would be used

    Returns:
    ---------
    latest_quote_id : str | None
        the latest quote's tweetId for the specific user
        if no quote was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    query: str
    if tweet_id is not None:
        query = f"{{tweetId: '{tweet_id}'}}"
    elif user_id is not None:
        query = f"{{authorId: '{user_id}'}}"
    else:
        raise ValueError("`tweet_id` and `user_id` are both None!")

    # latest quote as a dataframe
    df_latest_quote = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet {query})<-[r:QUOTED]-(m:Tweet)
        WHERE m.authorId <> t.authorId
        WITH MAX(SIZE(m.tweetId)) as max_size, m.tweetId as id
        RETURN MAX(id) as latest_quoted_id
        """
    )
    latest_quoted_id = df_latest_quote["latest_quoted_id"].iloc[0]

    return latest_quoted_id
