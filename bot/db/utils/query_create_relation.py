from .enums_data import Properties
from .update_value_by_type import make_val_by_type


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
    query += f"MERGE (a)-[r:{relation_name}]->(b) "

    # for properties
    if len(relation_properties) != 0:
        query += "SET "

    for idx, property in enumerate(relation_properties):
        val = make_val_by_type(property.property_value, property.property_format)
        query += f"r.{property.property_name}={val}"

        # if it wasn't the last index
        # add a comma to include the next property
        if idx + 1 != len(relation_properties):
            query += ", "

    return query
