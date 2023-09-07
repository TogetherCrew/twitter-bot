from datetime import datetime
from typing import Any

from .utils.query_create_entity import create_query

from .utils.enums_data import (
    NodeLabels,
    Properties,
    TwitterAccountProperties,
)
from tweepy import User


def create_twitter_user_profile_query(user_data: list[User]):
    """
    create the queries for saving user data into neo4j

    Parameters:
    ------------
    user_data : list[dict[str, Any]]
        the user profiles data to be saved

    Returns:
    ----------
    queries : list[str]
        the queries for inserting user data in neo4j
    """
    queries: list[str] = []

    for user in user_data:
        add_properties: list[Properties] = []
        if user["description"] is not None:
            # bio
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.bio,
                    property_value=user["description"],
                    property_format=str,
                )
            )
        # location
        if user["location"] is not None:
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.location,
                    property_value=user["location"],
                    property_format=str,
                )
            )
        # userName
        add_properties.append(
            Properties(
                property_name=TwitterAccountProperties.user_name,
                property_value=user["username"],
                property_format=str,
            )
        )
        # original name
        add_properties.append(
            Properties(
                property_name=TwitterAccountProperties.name,
                property_value=user["name"],
                property_format=str,
            )
        )
        if user["protected"] is not None:
            # account protected status
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.protected,
                    property_value=user["protected"],
                    property_format=bool,
                )
            )
        if user["profile_image_url"] is not None:
            # profile image
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.profile_image_url,
                    property_value=user["profile_image_url"],
                    property_format=str,
                )
            )
        if user["url"] is not None:
            # account url
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.url,
                    property_value=user["url"],
                    property_format=str,
                )
            )
        if user["verified"] is not None:
            # account verified
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.verified,
                    property_value=user["verified"],
                    property_format=bool,
                )
            )
        if user["created_at"] is not None:
            # creation date in twitter
            add_properties.append(
                Properties(
                    property_name=TwitterAccountProperties.created_at,
                    property_value=user["created_at"],
                    property_format=datetime,
                )
            )
        query = create_query(
            node_label=NodeLabels.twitter_account,
            merge_property=Properties(
                TwitterAccountProperties.user_id,
                user["id"],
                str,
            ),
            properties=add_properties,
        )

        queries.append(query)

    return queries
