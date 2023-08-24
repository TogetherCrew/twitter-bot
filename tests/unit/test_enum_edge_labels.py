from query_creator.enums_data import EdgeLabels


def test_enum_edge_labels():
    assert EdgeLabels.follows == "FOLLOWS"
    assert EdgeLabels.hashtagged == "HASHTAGGED"
    assert EdgeLabels.liked == "LIKED"
    assert EdgeLabels.mentioned == "MENTIONED"
    assert EdgeLabels.quoted == "QUOTED"
    assert EdgeLabels.retweeted == "RETWEETED"
    assert EdgeLabels.tweeted == "TWEETED"
    assert EdgeLabels.replied == "REPLIED"
