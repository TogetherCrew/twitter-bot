from .enums_data import Properties
from .update_value_by_type import make_val_by_type


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

    for idx, property in enumerate(properties):
        value = make_val_by_type(property.property_value, property.property_format)
        query += f"a.{property.property_name}={value}"

        if idx + 1 != len(properties):
            query += ", "

    return query