from datetime import datetime
from typing import Type


class BaseProperties:
    created_at: str = "createdAt"
    latest_saved_at: str = "latestSavedAt"


class TwitterAccountProperties:
    user_id: str = "userId"
    user_name: str = "userName"
    name: str = "name"
    bio: str = "bio"
    created_at: str = BaseProperties.created_at
    latest_saved_at: str = BaseProperties.latest_saved_at
    url: str = "url"
    profile_image_url: str = "profileImageUrl"
    verified: str = "verified"
    location: str = "location"
    protected: str = "protected"
    follower_count: str = "followerCount"
    following_count: str = "followingCount"


class TweetProperties:
    tweet_id: str = "tweetId"
    created_at: str = BaseProperties.created_at
    text: str = "text"
    like_counts: str = "likeCounts"
    image_url: str = "imageUrl"
    video_url: str = "videoUrl"
    author_id: str = "authorId"
    latest_saved_at: str = BaseProperties.latest_saved_at


class HashtagProperties:
    hashtag: str = "hashtag"
    created_at: str = BaseProperties.created_at
    latest_saved_at: str = BaseProperties.latest_saved_at


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
        self,
        property_name: str,
        property_value: str | list | datetime,
        property_format: Type[str] | Type[list] | Type[datetime] | Type[int],
    ) -> None:
        """
        The properties class for setting a property in a cypher query
        """
        self.property_name = property_name
        self.property_value = property_value
        self.property_format = property_format
