from bot.db.enums_data import NodeLabels, Properties, TweetProperties
from bot.db.utils import update_query


def test_update_query_single_add_properties():
    query = update_query(
        NodeLabels.tweet,
        match_properties=Properties(TweetProperties.author_id, "123321", str),
        add_properties=[Properties(TweetProperties.text, "Happy Day!", str)],
    )

    print(query)

    expected_query = """MERGE (a:Tweet {authorId: '123321'})"""
    expected_query += " SET a.text = 'Happy Day!'"
    assert expected_query in query


def test_update_query_multiple_add_properties():
    query = update_query(
        NodeLabels.tweet,
        match_properties=Properties(TweetProperties.author_id, "123321", str),
        add_properties=[
            Properties(TweetProperties.text, "Happy Day!", str),
            Properties(TweetProperties.like_counts, 5, int),
        ],
    )

    print(query)

    expected_query = """MERGE (a:Tweet {authorId: '123321'})"""
    expected_query += " SET a.text = 'Happy Day!', a.likeCounts = 5"
    assert expected_query in query
