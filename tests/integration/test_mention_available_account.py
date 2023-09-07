from datetime import datetime

from bot.db.twitter_data_to_cypher import create_twitter_data_query


def test_mention_available_account():
    """
    test users being mentioned but was created before
    so a query would be created to set values to them

    We're making a sample data that the user mention themselves
    """
    sample_data = {
        "id": "000000",
        "created_at": datetime.strptime(
            "2023-04-14 20:56:58+00:00", "%Y-%m-%d %H:%M:%S%z"
        ),
        "author_id": "123456",
        "author_bio": "amazing!",
        "conversation_id": "000000",
        "text": "SAMPLE_TEXT",
        "image_url": [],
        "video_url": [],
        "text_url": [],
        "type": [],
        "hashtags": [],
        "account_mentions": [{"username": "special_user", "id": "123456"}],
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 0,
            "reply_count": 0,
            "like_count": 0,
            "quote_count": 0,
            "impression_count": 0,
        },
        "context_annotations": [],
        "referenced_tweets": None,
    }

    queries = create_twitter_data_query([sample_data])

    query1 = """MERGE (a:Tweet {tweetId:"000000"}) """
    query1 += """MERGE (b:TwitterAccount {userId:"123456"}) """
    query1 += "MERGE (a)-[:MENTIONED {createdAt: 1681505818000}]->(b)"
    assert query1 in queries

    query2 = """MERGE (a:TwitterAccount {userId: "123456"}) """
    query2 += """SET a.userName="special_user" """
    query2 = query2[:-1]
    print("query2", query2)
    print("queries", queries)

    assert query2 in queries
