from query_creator.cypher_query_creator import create_twitter_data_query


def test_create_hashtags():
    sample_data = {
        "tweet_id": "000000",
        "created_at": "2023-04-14 20:56:58+00:00",
        "author_id": "123456",
        "author_bio": "amazing!",
        "conversation_id": "000000",
        "text": "FIND #web3 #jobs",
        "image_url": [],
        "video_url": [],
        "text_url": [],
        "type": ["retweeted"],
        "hashtags": ["web3", "jobs"],
        "account_mentions": [],
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 5,
            "reply_count": 0,
            "like_count": 0,
            "quote_count": 0,
            "impression_count": 0,
        },
        "context_annotations": [],
        "referenced_tweets": "[<ReferencedTweet id=567654 type=retweeted>]",
    }

    queries = create_twitter_data_query([sample_data])

    print(queries)

    query1 = "MERGE (a:Hashtag {hashtag: 'jobs'}) "
    assert query1 in queries

    query2 = "MERGE (a:Hashtag {hashtag: 'web3'}) "
    assert query2 in queries

    query3 = """MERGE (a:Tweet {tweetId:'000000'}) """
    query3 += """MERGE (b:Hashtag {hashtag:'jobs'}) """
    query3 += """MERGE (a)-[:HASHTAGGED {createdAt: 1681505818000}]->(b)"""
    assert query3 in queries

    query4 = """MERGE (a:Tweet {tweetId:'000000'}) """
    query4 += """MERGE (b:Hashtag {hashtag:'web3'}) """
    query4 += """MERGE (a)-[:HASHTAGGED {createdAt: 1681505818000}]->(b)"""
    assert query4 in queries
