import logging
from datetime import datetime, timezone
from typing import Type

from .enums_data import EdgeLabels, Properties


def create_query(
    node_label: str, merge_property: Properties, properties: list[Properties]
) -> str:
    """
    make a query to create a node with specific properties

    Parameters:
    ------------
    node_label : str
        the node label to create
    merge_property : Properties
        the property to first do the merge on it
        then we would add additional properties to the entity using `SET`
    properties : list[Properties]
        a list of properties to add to the creating node

    Returns:
    ---------
    query : str
        the query to do the node and its properties creation
    """
    query = f"MERGE (a:{node_label} "
    value = make_val_by_type(
        merge_property.property_value, merge_property.property_format
    )
    query += f"{{{merge_property.property_name}: {value}}}) "

    if len(properties) != 0:
        query += "SET "

    # query = f"CREATE (a:{node_label} " + "{"
    for idx, property in enumerate(properties):
        value = make_val_by_type(property.property_value, property.property_format)
        query += f"a.{property.property_name}={value}"

        if idx + 1 != len(properties):
            query += ", "

    return query


def update_query(
    node_label: str, match_properties: Properties, add_properties: list[Properties]
) -> str:
    """
    make a query to update a specific node
    (meaning to add proeprties to it)

    Parameters:
    ------------
    node_label : str
        the node label to add add_properties
    match_properties : Properties
        the properties to match the node on (finding node)
    add_properties : list[Properties]
        a list of peroperties to add to the matched node

    Returns:
    ---------
    query : str
        the query to update a node properties
    """
    val = make_val_by_type(
        match_properties.property_value, match_properties.property_format
    )
    query = f"MERGE (a:{node_label} {{{match_properties.property_name}: {val}}}) SET "
    for idx, attr in enumerate(add_properties):
        value = make_val_by_type(attr.property_value, attr.property_format)
        query += f"a.{attr.property_name} = {value}"

        if idx + 1 != len(add_properties):
            query += ", "

    return query


def relation_query(
    node_label1: str,
    node_label2: str,
    match_properties1: Properties,
    match_properties2: Properties,
    relation_name: str,
    relation_properties: list[Properties],
) -> str:
    """
    Create a relationship query between two nodes

    Parameters:
    ------------
    node_label1 : str
        the first node label
        this is the node which the edge come out from
    node_label2 : str
        the second node label
        this is the node which the edge come into it
    match_properties1 : Properties
        the attribute of the first node to do the match
    match_properties2 : Properties
        the attribute of the second node to do the match
    relation_name : str
        the relationship label
    relation_properties : list[Properties]
        the properties of relations

    Returns:
    ---------
    query : str
        the query that could make the relationship
    """
    val1 = make_val_by_type(
        match_properties1.property_value, match_properties1.property_format
    )
    val2 = make_val_by_type(
        match_properties2.property_value, match_properties2.property_format
    )

    query = f"MERGE (a:{node_label1} {{{match_properties1.property_name}:{val1}}}) "
    query += f"MERGE (b:{node_label2} {{{match_properties2.property_name}:{val2}}}) "
    query += f"MERGE (a)-[:{relation_name} "

    # for properties
    query += "{"
    for idx, property in enumerate(relation_properties):
        val = make_val_by_type(property.property_value, property.property_format)
        query += f"{property.property_name}: {val}"

        # if it wasn't the last index
        # add a comma to include the next property
        if idx + 1 != len(relation_properties):
            query += ", "

    query += "}]->(b)"

    return query


def make_val_by_type(
    value: str, type_val: Type[str] | Type[datetime] | Type[int] | Type[list]
) -> str | int | list:
    """
    In this function, we try to translate value based on the given type
    to which is acceptable for Cypehr in Neo4j

    Parameters:
    ------------
    value : str
        the string value to be converted to a given type of `type_val`
    type_val : str | int | datetime | list
        the value type for the string `value` to be converted

    Returns:
    ----------
    converted_data : str | int | list
        the converted data to be retuernd
        if datetime, the format must match `%Y-%m-%d %H:%M:%S%z`
    """
    converted_data: str | int | list

    if type_val is str:
        # def fix_quotation_marks(text):
        #     if type(text) == str:
        #         fixed_text = text.replace('"', r"\"")
        #         return fixed_text
        #     return None

        # value = fix_quotation_marks(value)
        if type(value) is str:
            # converted_data = '"' + value + '"'
            converted_data = value.replace("'", '"')
            converted_data = r"'{}'".format(converted_data)
        else:
            msg = f"given value '{value}' is not string!, type: {type(value)}"
            msg += " Trying to convert to string!"
            try:
                converted_data = str(value)
            except Exception as exp:
                logging.error(exp)
                logging.error("defaulting to save empty text")
                converted_data = '"'

    elif type_val is int:
        converted_data = int(value)

    elif type_val is datetime:
        # for time we using UTC time
        datetime_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S%z")
        datetime_obj_utc = datetime_obj.replace(tzinfo=timezone.utc)
        converted_data = int(datetime_obj_utc.timestamp() * 1000)

    elif type_val is list:
        # ans = "["
        # for a in value:
        #     # ans += '"' + str(a) + '",'
        #     ans += r"'{}',".format(a)
        # ans = ans[:-1]
        # ans += "]"
        # converted_data = ans
        converted_data = r"{}".format(value)

    return converted_data


def tweet_type_finder(data_type: str) -> tuple[str, str]:
    """
    gives refrence data_type of tweet and it finds out
    Is it retweet or reply or quote
    It is a sample:
    "[<ReferencedTweet id=1633929436260364288 type=retweeted>]"
    types:{
        quoted,
        retweeted,
        replied_to
    }

    Parameters:
    ------------
    data_type : str
        the given type from data

    Returns:
    ---------
    id_value : str
        the id of the tweet
    type_value : str
        the type of tweet
    """
    id_start = data_type.find("id=") + 3
    id_end = data_type.find(" ", id_start)
    id_value = data_type[id_start:id_end]

    type_start = data_type.find("type=") + 5
    type_end = data_type.find(">", type_start)
    type_value = data_type[type_start:type_end]

    if type_value == "quoted":
        type_value = EdgeLabels.quoted
    elif type_value == "retweeted":
        type_value = EdgeLabels.retweeted
    elif type_value == "replied_to":
        type_value = EdgeLabels.replied

    return id_value, type_value
