from datetime import datetime

from tweepy import ReferencedTweet

from bot.db.twitter_data_to_cypher import create_twitter_data_query


def test_reply_query():
    sample_data = {
        "id": "000000",
        "created_at": datetime.strptime(
            "2022-12-26 14:35:13+00:00", "%Y-%m-%d %H:%M:%S%z"
        ),
        "author_id": "12345",
        "author_bio": "he's bio!",
        "conversation_id": "8765432",
        "text": "@user I think you look great!",
        "image_url": [],
        "video_url": [],
        "text_url": [],
        "type": ["replied_to"],
        "hashtags": [],
        "account_mentions": [{"username": "user", "id": "535353"}],
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 0,
            "reply_count": 0,
            "like_count": 0,
            "quote_count": 0,
            "impression_count": 199,
        },
        "context_annotations": [],
        "referenced_tweets": [
            ReferencedTweet(data={"id": 8765432, "type": "replied_to"})
        ],
    }

    queries = create_twitter_data_query([sample_data])

    query = """MERGE (a:Tweet {tweetId:"000000"}) """
    query += """MERGE (b:Tweet {tweetId:"8765432"}) """
    query += "MERGE (a)-[:REPLIED {createdAt: 1672065313000}]->(b)"

    assert query in queries

    query2 = """MERGE (a:Tweet {tweetId:"000000"}) """
    query2 += """MERGE (b:TwitterAccount {userId:"535353"}) """
    query2 += "MERGE (a)-[:MENTIONED {createdAt: 1672065313000}]->(b)"
