from query_creator.enums_data import BaseProperties


def test_base_properties():
    assert BaseProperties.created_at == "createdAt"
