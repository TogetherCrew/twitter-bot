import functools
import logging

from itertools import count


def retry_function_if_fail(func, /, *args, **keywords):
    retry_number = (
        keywords["retry_number"] if "retry_number" in keywords else 5
    )  # default retry number
    function = functools.partial(func, *args, **keywords)
    for counter in count(1):
        try:
            response = function()
            return response

        except Exception as ex:
            logging.error(f"[Exception(retry_function_if_fail)]: {ex}")

        finally:
            if counter == retry_number:
                raise RuntimeError(
                    "Something went wrong when communicating with Twitter"
                )


class FetchConfigs:
    max_like_results = 100
    max_tweet_results = 100

    tweet_fields = [
        "id",
        "text",
        "entities",
        "created_at",
        "author_id",
        "conversation_id",
        "public_metrics",
        "referenced_tweets",
        "context_annotations",
        "in_reply_to_user_id",
    ]

    user_fields = [
        "id",
        "name",
        "username",
        "created_at",
        "public_metrics",
        "description",
        "location",
        "profile_image_url",
        "protected",
        "url",
        "verified",
    ]
