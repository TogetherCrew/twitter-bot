from query_creator.cypher_query_creator import create_twitter_data_query


def test_create_tweeted_person():
    """
    create queries for a person that tweets a tweet (relationships included)
    """
    sample_data = [
        {
            "tweet_id": "000000",
            "created_at": "2023-03-17 23:19:30+00:00",
            "author_id": "89129821",
            "author_bio": "We're together in togetherCrew",
            "conversation_id": "000000",
            "text": "samplesamplesample",
            "image_url": [],
            "video_url": [],
            "text_url": [],
            "type": [],
            "hashtags": [],
            "account_mentions": [
                {"username": "iqwe2qw", "id": "1111111"},
                {"username": "tashhfa", "id": "222222"},
            ],
            "cashtags": [],
            "public_metrics": {
                "retweet_count": 3,
                "reply_count": 0,
                "like_count": 15,
                "quote_count": 0,
                "impression_count": 1632,
            },
            "context_annotations": [
                {
                    "domain": {
                        "id": "46",
                        "name": "A1",
                        "description": "A1 description",
                    },
                    "entity": {
                        "id": "333333",
                        "name": "A2",
                        "description": "A2 description",
                    },
                },
                {
                    "domain": {
                        "id": "44",
                        "name": "A3",
                        "description": "A3 description",
                    },
                    "entity": {"id": "1461476432551366659", "name": "O1"},
                },
                {
                    "domain": {
                        "id": "44",
                        "name": "A4",
                        "description": "A4 description",
                    },
                    "entity": {
                        "id": "555555",
                        "name": "A5",
                        "description": "A5 description",
                    },
                },
            ],
            "referenced_tweets": None,
        },
        {
            "tweet_id": "66666666",
            "created_at": "2023-03-10 18:43:42+00:00",
            "author_id": "89129821",
            "author_bio": "We're together in togetherCrew",
            "conversation_id": "66666666",
            "text": "RT sample",
            "image_url": [],
            "video_url": [],
            "text_url": [],
            "type": ["retweeted"],
            "hashtags": [],
            "account_mentions": [
                {"username": "Ac1", "id": "567893212"},
                {"username": "Ac2", "id": "09458723"},
            ],
            "cashtags": [],
            "public_metrics": {
                "retweet_count": 4,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0,
                "impression_count": 0,
            },
            "context_annotations": [
                {
                    "domain": {
                        "id": "765",
                        "name": "AA1",
                        "description": "AA1 descriptoin",
                    },
                    "entity": {"id": "523872389", "name": "Twitter"},
                }
            ],
            "referenced_tweets": "[<ReferencedTweet id=8374981 type=retweeted>]",
        },
    ]

    queries = create_twitter_data_query(sample_data)

    print(queries)
    query1 = """CREATE (a:Tweet {tweetId: '000000', createdAt: 1679095170000, """
    query1 += "authorId: '89129821', text: 'samplesamplesample', "
    query1 += "likeCounts: 15})"

    assert query1 in queries

    query2 = "CREATE (a:TwitterAccount {userId: '89129821', "
    query2 += """bio: 'We"re together in togetherCrew'})"""

    assert query2 in queries

    query3 = "MERGE (a:TwitterAccount {userId:'89129821'}) "
    query3 += "MERGE (b:Tweet {tweetId:'000000'}) "
    query3 += "MERGE (a)-[:TWEETED {createdAt: 1679095170000}]->(b)"

    assert query3 in queries

    query4 = "CREATE (a:TwitterAccount {userId: '1111111', userName: 'iqwe2qw'})"

    assert query4 in queries

    query5 = "MERGE (a:Tweet {tweetId:'000000'}) "
    query5 += "MERGE (b:TwitterAccount {userId:'1111111'}) "
    query5 += "MERGE (a)-[:MENTIONED {createdAt: 1679095170000}]->(b)"

    assert query5 in queries

    query6 = """CREATE (a:TwitterAccount {userId: '222222', userName: 'tashhfa'})"""
    assert query6 in queries

    query7 = "CREATE (a:Tweet {tweetId: '66666666', createdAt: 1678473822000, "
    query7 += "authorId: '89129821', text: 'RT sample', likeCounts: 0})"

    assert query7 in queries

    query8 = "MERGE (a:TwitterAccount {userId: '89129821'}) "
    query8 += """SET a.bio = 'We"re together in togetherCrew'"""
    assert query8 in queries

    query9 = "CREATE (a:TwitterAccount {userId: '567893212', userName: 'Ac1'})"
    assert query9 in queries

    query10 = "CREATE (a:TwitterAccount {userId: '09458723', userName: 'Ac2'})"
    assert query10 in queries

    query11 = "MERGE (a:Tweet {tweetId:'66666666'}) "
    query11 += "MERGE (b:Tweet {tweetId:'8374981'}) "
    query11 += "MERGE (a)-[:RETWEETED {createdAt: 1678473822000}]->(b)"

    assert query11 in queries
