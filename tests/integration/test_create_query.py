from datetime import datetime
from query_creator.enums_data import NodeLabels, Properties, TwitterAccountProperties
from query_creator.utils import create_query


def test_create_query_single_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        properties=[
            Properties(TwitterAccountProperties.user_name, "sepehr", str),
        ],
    )

    print(query)
    assert query == """CREATE (a:TwitterAccount {userName: 'sepehr'})"""


def test_create_query_double_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        properties=[
            Properties(TwitterAccountProperties.user_name, "sepehr", str),
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
        ],
    )

    print(query)
    assert (
        query
        == """CREATE (a:TwitterAccount {userName: 'sepehr', bio: 'My Age is 22 :)'})"""
    )


def test_create_query_multiple_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        properties=[
            Properties(TwitterAccountProperties.user_name, "sepehr", str),
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
            Properties(TwitterAccountProperties.user_id, "123456", str),
            Properties(
                TwitterAccountProperties.created_at,
                "2023-04-17 14:03:55+00:00",
                datetime,
            ),
        ],
    )

    print(query)
    assert (  # flake8: noqa
        query
        == """CREATE (a:TwitterAccount {userName: 'sepehr', bio: 'My Age is 22 :)', userId: '123456', createdAt: 1681740235000})"""
    )
