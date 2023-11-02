import argparse
import logging

import tweepy
from bot.db.analytics.advanced_analytics import AdvancedAnalytics
from bot.db.analytics.simple_analytics import SimpleAnalytics
from bot.services.user_info import get_twitter_user
from bot.twitter import (
    extract_and_save_liked_tweets,
    extract_and_save_liker_users,
    extract_and_save_tweets,
    extract_and_save_user_information,
)

bold_style = "\033[1m"
end_style = "\033[0m"


def extract_and_save(user: tweepy.User) -> None:
    """
    extract and save the twitter raw data into database

    Parameters
    ------------
    username : tweepy.User
        the twitter username which could be for example `sample_user`
    """
    logging.info(f"{bold_style}Starting Job 1 (Tweets Extraction){end_style}")
    extract_and_save_tweets(username=user.username)

    logging.info(f"{bold_style}Starting Job 2 (Likes Extraction){end_style}")
    extract_and_save_liked_tweets(user_id=user.id)
    extract_and_save_liker_users(user_id=user.id)

    logging.info(f"{bold_style}Starting Job 3 (Completing missing profiles){end_style}")
    extract_and_save_user_information(user_id=str(user.id))


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("twitter_username")
    args = parser.parse_args()
    username = args.twitter_username

    user = get_twitter_user(username=username)

    logging.info(f"{bold_style}Username:{end_style} {username}")
    logging.info(f"{bold_style}UserId:{end_style} {user.id}")
    logging.info(f"{bold_style}Starting the extraction process{end_style}")
    logging.info(
        f"{bold_style}Extraction (& Saving) process will be with the order of {end_style}"
    )
    logging.info(f"{bold_style}1. Tweets extraction {end_style}")
    logging.info(
        f"{bold_style}2. Likes extraction (both user's like and other users liking the posts){end_style}"
    )
    logging.info(f"{bold_style}3. Completing missing profiles{end_style}")
    logging.info("-" * 25)

    # doing extraction and saving
    extract_and_save(user)

    logging.info("-" * 25)
    # showing analytics results

    logging.info(f"{bold_style}Account Activity{end_style}")
    simple_analytics = SimpleAnalytics(user_id=user.id)
    (
        engagement_acc_count,
        follower_count,
    ) = simple_analytics.get_account_overview(user_id=user.id)
    logging.info(
        f"Total count of Accounts that engage with you: {engagement_acc_count}"
    )
    logging.info(f"Follower count: {follower_count}")

    logging.info(f"{bold_style}Your account activity{end_style}")
    (
        tweet_count,
        reply_count,
        retweet_count,
        # like_count,
        mention_count,
    ) = simple_analytics.get_user_account_activity(user_id=user.id)
    logging.info(f"Number of tweets the user made: {tweet_count}")
    logging.info(f"Number of replies the user made: {reply_count}")
    logging.info(f"Number of retweets the user made: {retweet_count}")
    # logging.info(f"Number of likes the user made: {like_count}")
    logging.info(f"Number of mentions the user made: {mention_count}")

    logging.info(f"{bold_style}Audience Response{end_style}")
    (
        replies_count,
        retweets_count,
        likes_count,
        mentions_count,
    ) = simple_analytics.get_audience_response(user_id=user.id)
    logging.info(f"Count of replies others made on the user's posts: {replies_count}")
    logging.info(f"Count of retweets others made on the user's posts: {retweets_count}")
    logging.info(f"Count of likes others made on the user's posts: {likes_count}")
    logging.info(f"Number of times being mentioned: {mentions_count}")

    logging.info(f"{bold_style}Engagement by account{end_style}")

    advanced_analytics = AdvancedAnalytics(user_id=user.id)
    (
        analytics_1,
        analytics_2,
        analytics_3,
        analytics_4,
    ) = advanced_analytics.get_engagement_by_account_counts(user_id=user.id)
    logging.info(
        f"Accounts count that only engaged a bit but deeper interactions: {analytics_1}"
    )
    logging.info(
        f"Accounts count that frequently engaged and deep interactions: {analytics_2}"
    )
    logging.info(
        f"Accounts count that only engaged a bit and shallow interactions: {analytics_3}"
    )
    logging.info(
        f"Accounts count that frequently engaged but shallow interactions: {analytics_4}"
    )
