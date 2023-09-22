from bot.db.utils.enums_data import TweetProperties


def test_enum_tweet_properties():
    assert TweetProperties.author_id == "authorId"
    assert TweetProperties.created_at == "createdAt"
    assert TweetProperties.image_url == "imageUrl"
    assert TweetProperties.video_url == "videoUrl"
    assert TweetProperties.like_counts == "likeCounts"
    assert TweetProperties.text == "text"
    assert TweetProperties.tweet_id == "tweetId"
