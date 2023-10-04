from datetime import datetime, timedelta, timezone

from bot.utils.get_epoch import get_x_days_ago_UTC_timestamp

from .neo4j_connection import Neo4jConnection


def get_latest_tweet_since(
    user_id: str, since: int = get_x_days_ago_UTC_timestamp(7)
) -> str | None:
    """
    get the user handle to get their latest mantion's tweetId

    Parameters:
    ------------
    user_id : str
        given the userId, find the required information
    since : int
        UTC timestamp epoch
        default is 7 days ago UTC timestamp from now

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
        WHERE m.createdAt >= {since}
        WITH MAX(SIZE(m.tweetId)) as max_size, m.tweetId as id
        RETURN MAX(id) as latest_tweeted_id
        """
    )
    latest_tweeted_id = df_latest_tweeted["latest_tweeted_id"].iloc[0]

    return latest_tweeted_id


def get_days_ago_tweet_ids(user_id: str, days: int = 7) -> list[str]:
    """
    get the tweetIds of a user for given days ago

    Parameters:
    ------------
    user_id : str
        the twitter account id
    days : int
        the count of days ago tweetIds to get
        default is `7` meaning 7 days ago

    Returns:
    ---------
    tweet_ids : list[str]
        a list of tweet ids for the user
        the ids can be related to either tweet, reply, quote, or retweet
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # the past `days` timestamp
    epoch_past = (
        datetime.now().replace(
            hour=0, minute=0, microsecond=0, second=0, tzinfo=timezone.utc
        )
        - timedelta(days=days)
    ).timestamp() * 1000

    # latest tweet id as a dataframe
    df_tweet_ids = gds.run_cypher(
        f"""
        MATCH (t:Tweet {{authorId: '{user_id}'}})
        WHERE t.createdAt >= {epoch_past}
        RETURN t.tweetId as tweet_ids
        """
    )
    tweet_ids = df_tweet_ids["tweet_ids"].values

    return list(tweet_ids)
