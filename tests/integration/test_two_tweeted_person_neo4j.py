from bot.db.neo4j_connection import Neo4jConnection
from bot.db.twitter_data_to_cypher import create_twitter_data_query
from tweepy import ReferencedTweet

from datetime import datetime


def test_create_two_person_tweeted_neo4j():
    """
    create queries for a person that tweets a tweet (relationships included)
    """
    sample_data = [
        {
            "id": "000000",
            "created_at": datetime.strptime(
                "2023-03-17 23:19:30+00:00", "%Y-%m-%d %H:%M:%S%z"
            ),
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
            "id": "66666666",
            "created_at": datetime.strptime(
                "2023-03-10 18:43:42+00:00", "%Y-%m-%d %H:%M:%S%z"
            ),
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
            "referenced_tweets": [
                ReferencedTweet(data={"id": 8374981, "type": "retweeted"})
            ],
        },
    ]

    queries = create_twitter_data_query(sample_data)

    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(queries, message="test_create_two_person_tweeted_neo4j")
    print(queries)

    results_tweeted = neo4j_ops.gds.run_cypher(
        """
        MATCH
            (a:TwitterAccount {userId: '89129821'})
                -[r:TWEETED] -> (b:Tweet {tweetId: '000000'})
        RETURN
            a{.*} as account,
            r{.*} as tweeted,
            b{.*} as tweet
        """
    )
    assert len(results_tweeted) == 1
    for _, row in results_tweeted.iterrows():
        account = row["account"]
        tweeted_rel = row["tweeted"]
        tweet = row["tweet"]

        assert account["userId"] == "89129821"
        assert account["bio"] == """We're together in togetherCrew"""

        assert tweeted_rel["createdAt"] == 1679095170000

        assert tweet["tweetId"] == "000000"
        assert tweet["text"] == "samplesamplesample"
        assert tweet["authorId"] == "89129821"
        assert tweet["likeCounts"] == 15

    results_mentioned = neo4j_ops.gds.run_cypher(
        """
        MATCH
            (a:Tweet {tweetId: '000000'})
                -[r:MENTIONED] -> (b:TwitterAccount {userId: '1111111'})
        RETURN
            r{.*} as mentioned,
            b{.*} as account
        """
    )
    assert len(results_mentioned) == 1
    for _, row in results_mentioned.iterrows():
        account = row["account"]
        mentioned_rel = row["mentioned"]

        assert account["userId"] == "1111111"
        assert account["userName"] == "iqwe2qw"

        assert mentioned_rel["createdAt"] == 1679095170000

    results_retweeted = neo4j_ops.gds.run_cypher(
        """
        MATCH
            (a:Tweet {tweetId: '66666666'})
                -[r:RETWEETED] -> (b:Tweet {tweetId: '8374981'})
        RETURN
            a{.*} as source,
            r{.*} as retweeted,
            b{.*} as target
        """
    )
    assert len(results_retweeted) == 1
    for _, row in results_retweeted.iterrows():
        acc_source = row["source"]
        acc_target = row["target"]

        retweeted_rel = row["retweeted"]

        assert acc_source["tweetId"] == "66666666"
        assert acc_source["authorId"] == "89129821"
        assert acc_source["text"] == "RT sample"

        assert acc_target["tweetId"] == "8374981"
        assert "authorId" not in acc_target
        assert "text" not in acc_target

        assert retweeted_rel["createdAt"] == 1678473822000
