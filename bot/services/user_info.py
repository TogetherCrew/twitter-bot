import tweepy

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_twitter_user(id=None, username=None) -> tweepy.User:
    if id is not None and username is not None:
        raise TypeError("Expected ID or username, not both")

    user = retry_function_if_fail(
        TwitterClient.client.get_user,
        id=id,
        username=username,
        user_fields=FetchConfigs.user_fields,
    )

    user_data: tweepy.User = user.data
    return user_data


def get_twitter_users(ids=None, usernames=None) -> list[tweepy.User]:
    if ids is not None and usernames is not None:
        raise TypeError("Expected IDs or usernames, not both")

    ids = ",".join(ids) if ids else None
    usernames = ",".join(usernames) if usernames else None

    users = retry_function_if_fail(
        TwitterClient.client.get_users,
        ids=ids,
        usernames=usernames,
        user_fields=FetchConfigs.user_fields,
    )

    user_data: list[tweepy.User] = users.data
    return user_data
