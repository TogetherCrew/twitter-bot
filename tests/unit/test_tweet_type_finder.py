from bot.db.utils import tweet_type_finder


def test_tweet_type_finder_replied():
    data = "[<ReferencedTweet id=123456 type=replied_to>]"
    id, d_type = tweet_type_finder(data)

    assert id == "123456"
    assert d_type == "REPLIED"


def test_tweet_type_finder_retweet():
    data = "[<ReferencedTweet id=56789765 type=retweeted>]"
    id, d_type = tweet_type_finder(data)

    assert id == "56789765"
    assert d_type == "RETWEETED"


def test_tweet_type_finder_quote():
    data = "[<ReferencedTweet id=876543 type=quoted>]"
    id, d_type = tweet_type_finder(data)

    assert id == "876543"
    assert d_type == "QUOTED"
