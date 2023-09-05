from bot.db.utils.enums_data import HashtagProperties


def test_enum_hashtag_properties():
    assert HashtagProperties.created_at == "createdAt"
    assert HashtagProperties.hashtag == "hashtag"
