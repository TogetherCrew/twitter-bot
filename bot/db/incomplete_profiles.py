from .neo4j_connection import Neo4jConnection


def get_incomplete_profile_ids(by: str = "userName") -> list[str]:
    """
    get the id of TwitterAccounts with incomplete profile data

    Parameters:
    ------------
    by : str
        search if the field was not available return the userIds of those users
        default is `userName`. can be other fields that always apear in user data

    Returns:
    --------
    incomplete_profile_ids : list[str]
        the ids of TwitterAccounts with incomplete profile
    """
    neo4j_connection = Neo4jConnection()
    gds = neo4j_connection.neo4j_ops.gds

    # dataframe of incomplete profile ids
    df_incomplete_profiles = gds.run_cypher(
        f"""
        MATCH (a:TwitterAccount)
        WHERE a.{by} IS NULL
        RETURN a.userId as incomplete_profile_ids
        """
    )
    incomplete_profile_ids = df_incomplete_profiles["incomplete_profile_ids"].values

    return list(incomplete_profile_ids)
