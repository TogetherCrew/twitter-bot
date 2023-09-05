from bot.db.utils.enums_data import TwitterAccountProperties


def test_enum_twitter_account_properties():
    assert TwitterAccountProperties.bio == "bio"
    assert TwitterAccountProperties.created_at == "createdAt"
    assert TwitterAccountProperties.user_id == "userId"
    assert TwitterAccountProperties.user_name == "userName"
