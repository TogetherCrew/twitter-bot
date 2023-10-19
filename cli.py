import argparse
import logging

import tweepy

from bot.twitter import (
    extract_and_save_liked_tweets,
    extract_and_save_liker_users,
    extract_and_save_tweets,
    extract_and_save_user_information,
)
from bot.services.user_info import get_twitter_user



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

    logging.info(f"{bold_style}Starting Job 3 (Completing missing profiles)")
    extract_and_save_user_information(user_id=user.id)


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

    bold_style = "\033[1m"
    end_style = "\033[0m"
    logging.info(f"{bold_style}Inserted username:{end_style} {username}")
    logging.info(f"{bold_style}Starting the extraction process")
    logging.info(
        f"{bold_style}Extraction (& Saving) process will be with the order of {end_style}"
    )
    logging.info(f"{bold_style}1. Tweets extraction {end_style}")
    logging.info(
        f"{bold_style}2. Likes extraction (both user's like and other users liking the posts){end_style}"
    )
    logging.info(f"{bold_style}3. Completing missing profiles{end_style}")
    logging.info("-"* 25)

    

    extract_and_save(user)


