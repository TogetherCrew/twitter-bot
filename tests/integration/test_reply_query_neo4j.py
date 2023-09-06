from bot.db.neo4j_connection import Neo4jConnection
from bot.db.twitter_data_to_cypher import create_twitter_data_query
from datetime import datetime

from tweepy import ReferencedTweet

def test_reply_query_neo4j():
    sample_data = {
        "id": "000000",
        "created_at": datetime.strptime(
            "2022-12-26 14:35:13+00:00", 
            "%Y-%m-%d %H:%M:%S%z"
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
        "referenced_tweets": [ReferencedTweet(data={
            'id': 8765432,
            'type': 'replied_to'
        })]
    }

    queries = create_twitter_data_query([sample_data])
    print(queries)
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(queries, message="test_reply_query_neo4j")

    results_reply = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:Tweet {tweetId:'000000'}) -[r:REPLIED]-> (b:Tweet {tweetId:'8765432'})
        RETURN r{.*} as reply
        """
    )
    assert len(results_reply) == 1
    data = results_reply["reply"].values[0]
    assert data["createdAt"] == 1672065313000

    results_mention = neo4j_ops.gds.run_cypher(
        """
        MATCH
            (a:Tweet {tweetId: '000000'})
                -[r:MENTIONED]->(:TwitterAccount {userId: '535353'})
        RETURN r{.*} as mention
        """
    )
    assert len(results_mention) == 1
    data = results_mention["mention"].values[0]
    assert data["createdAt"] == 1672065313000
