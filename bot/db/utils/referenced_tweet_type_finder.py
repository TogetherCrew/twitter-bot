from .enums_data import EdgeLabels


def tweet_type_finder(referenced_tweet: dict[str, str]) -> tuple[str, str]:
    """
    gives refrence data_type of tweet and it finds out
    Is it retweet or reply or quote
    It is a sample:
    "[<ReferencedTweet id=1633929436260364288 type=retweeted>]"
    types:{
        quoted,
        retweeted,
        replied_to
    }

    Parameters:
    ------------
    referenced_tweet : dict[str, str]
        the given type from data

    Returns:
    ---------
    id_value : str
        the id of the tweet
    type_value : str
        the type of tweet
    """
    id_value = str(referenced_tweet["id"])
    type_value = referenced_tweet["type"]

    if type_value == "quoted":
        type_value = EdgeLabels.quoted
    elif type_value == "retweeted":
        type_value = EdgeLabels.retweeted
    elif type_value == "replied_to":
        type_value = EdgeLabels.replied

    return id_value, type_value
