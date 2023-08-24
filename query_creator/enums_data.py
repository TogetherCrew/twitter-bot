class BaseProperties:
    created_at: str = "createdAt"


class TwitterAccountProperties:
    user_id: str = "userId"
    user_name: str = "userName"
    bio: str = "bio"
    created_at: str = BaseProperties.created_at


class TweetProperties:
    tweet_id: str = "tweetId"
    created_at: str = BaseProperties.created_at
    text: str = "text"
    like_counts: str = "likeCounts"
    image_url: str = "imageUrl"
    video_url: str = "videoUrl"
    author_id: str = "authorId"


class HashtagProperties:
    hashtag: str = "hashtag"
    created_at: str = BaseProperties.created_at


class NodeLabels:
    twitter_account: str = "TwitterAccount"
    tweet: str = "Tweet"
    hashtag: str = "Hashtag"


class EdgeLabels:
    tweeted: str = "TWEETED"
    quoted: str = "QUOTED"
    replied: str = "REPLIED"
    retweeted: str = "RETWEETED"
    mentioned: str = "MENTIONED"
    hashtagged: str = "HASHTAGGED"
    follows: str = "FOLLOWS"
    liked: str = "LIKED"


class Properties:
    def __init__(
        self, property_name: str, property_value: str, property_format: str
    ) -> None:
        """
        The properties class for setting a property in a cypher query
        """
        self.property_name = property_name
        self.property_value = property_value
        self.property_format = property_format
