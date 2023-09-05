from query_creator.enums_data import NodeLabels


def test_enum_node_labels():
    assert NodeLabels.hashtag == "Hashtag"
    assert NodeLabels.tweet == "Tweet"
    assert NodeLabels.twitter_account == "TwitterAccount"
