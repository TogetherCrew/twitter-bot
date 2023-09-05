from .neo4j_connection import Neo4jConnection

def get_latest_reply(
        user_id : str, 
    ) -> str:
    """
    get the user handle to get their latest reply's tweetId

    Parameters:
    ------------
    user_id : str | None
        given the userId, find the required information

    Returns:
    ---------
    latest_reply_id : str | None
        the latest reply's tweetId for the specific user
        if no reply was available, then None will be returned
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # latest reply as a dataframe
    df_latest_reply = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:REPLIED]-(m:Tweet)
        WHERE m.authorId <> '{user_id}'
        RETURN toString(MAX(toInteger(t.tweetId))) as latest_reply_id
        """
    )
    latest_reply_id = df_latest_reply["latest_reply_id"].iloc[0]

    return latest_reply_id

