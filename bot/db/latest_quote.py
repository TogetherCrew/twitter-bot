from .neo4j_connection import Neo4jConnection

def get_latest_quote(
        user_id : str, 
    ) -> str:
    """
    get the user handle to get their latest quote's tweetId

    Parameters:
    ------------
    user_id : str | None
        given the userId, find the required information

    Returns:
    ---------
    latest_quote_id : str | None
        the latest quote's tweetId for the specific user
        if no quote was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # latest quote as a dataframe
    df_latest_quote = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:QUOTED]-(m:Tweet)
        WHERE m.authorId <> '{user_id}'
        RETURN toString(MAX(toInteger(m.tweetId))) as latest_quoted_id
        """
    )
    latest_quoted_id = df_latest_quote["latest_quoted_id"].iloc[0]

    return latest_quoted_id


