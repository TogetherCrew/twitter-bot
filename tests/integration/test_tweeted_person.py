from query_creator.cypher_query_creator import create_twitter_data_query


def test_create_tweeted_person():
    """
    create queries for a person that tweets a tweet (relationships included)
    """
    sample_data = {
        "tweet_id": "0000",
        "created_at": "2023-04-13 01:21:51+00:00",
        "author_id": "12344321",
        "author_bio": "Amazing man with a perfect profile!",
        "conversation_id": "0000",
        "text": "IYKYK - @user2 https://somelink",
        "image_url": ["https://twitter.com/amazingman/status/0000/photo/1"],
        "video_url": ["https://twitter.com/amazingman/status/0000/video/1"],
        "text_url": [],
        "type": [],
        "hashtags": [],
        "account_mentions": [{"username": "user2", "id": "987789"}],
        "cashtags": [],
        "public_metrics": {
            "retweet_count": 1,
            "reply_count": 0,
            "like_count": 5,
            "quote_count": 0,
            "impression_count": 415,
        },
        "context_annotations": [],
        "referenced_tweets": None,
    }

    queries = create_twitter_data_query([sample_data])

    print(queries)
    query1 = """CREATE (a:Tweet {tweetId: '0000', createdAt: 1681348911000, """
    query1 += f"authorId: '12344321', text: '{sample_data['text']}', "
    query1 += f"""likeCounts: 5, imageUrl: {str(sample_data['image_url'])}, """
    query1 += f"""videoUrl: {str(sample_data['video_url'])}}})"""

    assert query1 in queries

    query2 = "CREATE (a:TwitterAccount {userId: '12344321', "
    query2 += "bio: 'Amazing man with a perfect profile!'})"

    assert query2 in queries

    query3 = "MATCH (a:TwitterAccount {userId:'12344321'}), "
    query3 += "(b:Tweet {tweetId:'0000'}) "
    query3 += "MERGE (a)-[:TWEETED {createdAt: 1681348911000}]->(b)"

    assert query3 in queries

    query4 = "CREATE (a:TwitterAccount {userId: '987789', userName: 'user2'})"

    assert query4 in queries

    query5 = "MATCH (a:Tweet {tweetId:'0000'}), "
    query5 += "(b:TwitterAccount {userId:'987789'}) "
    query5 += "MERGE (a)-[:MENTIONED {createdAt: 1681348911000}]->(b)"

    assert query5 in queries
