from bot.utils.get_epoch import get_x_days_ago_UTC_timestamp

from .neo4j_connection import Neo4jConnection


def get_latest_reply_since(
    user_id: str | None = None, 
    tweet_id: str | None = None,
    since: int = get_x_days_ago_UTC_timestamp(7)
) -> str | None:
    """
    get the user handle to get their latest reply's tweetId
    or using the tweet_id find its latest reply

    Parameters:
    ------------
    user_id : str | None
        given the userId, find the required information
    since : int
        UTC timestamp epoch
        default is 7 days ago UTC timestamp from now

    Returns:
    ---------
    latest_reply_id : str | None
        the latest reply's tweetId for the specific user
        if no reply was available, then None will be returned
    """
    query: str
    if tweet_id is not None:
        query = f"{{tweetId: '{tweet_id}'}}"
    elif user_id is not None:
        query = f"{{authorId: '{user_id}'}}"
    else:
        raise ValueError("`tweet_id` and `user_id` are both None!")

    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # latest reply as a dataframe
    df_latest_reply = gds.run_cypher(
        f"""
        OPTIONAL MATCH (t:Tweet {query})<-[r:REPLIED]-(m:Tweet)
        WHERE r.createdAt >= {since}
        WITH MAX(SIZE(m.tweetId)) as max_size, m.tweetId as id
        RETURN MAX(id) as latest_reply_id
        """
    )
    latest_reply_id = df_latest_reply["latest_reply_id"].iloc[0]

    return latest_reply_id
