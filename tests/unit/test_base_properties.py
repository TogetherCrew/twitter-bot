from bot.db.enums_data import BaseProperties


def test_base_properties():
    assert BaseProperties.created_at == "createdAt"
