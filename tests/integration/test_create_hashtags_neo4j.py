from query_creator.cypher_query_creator import create_twitter_data_query
from neo4j_connection import connect_neo4j


def test_create_hashtags_neo4j():
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

    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(query_list=queries, message="test_create_hashtags")

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (h:Hashtag)
        RETURN
        h{.*} as h
        """
    )
    for _, row in results.iterrows():
        assert row["h"]["hashtag"] in ["web3", "jobs"]
