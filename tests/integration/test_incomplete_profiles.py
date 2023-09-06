from bot.db.incomplete_profiles import get_incomplete_profile_ids
from bot.db.neo4j_connection import Neo4jConnection


def test_incomplete_profiles_no_data_no_ouptut():
    """
    get no id in case of no data in database
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    ids = get_incomplete_profile_ids()

    assert ids is not None
    assert ids == []


def test_incomplete_profiles_no_outputs():
    """
    get no id in case of all profiles are complete
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.gds.run_cypher(
        """
        MERGE (:TwitterAccount {
            userId: '111', 
            userName: 'Tom', 
            bio: 'some guy from LA',
            createdAt: 10000000
        })
        MERGE (:TwitterAccount {
            userId: '112', 
            userName: 'Jerry', 
            bio: 'some guy from NC',
            createdAt: 10000001
        })
        MERGE (:TwitterAccount {
            userId: '113', 
            userName: 'Tuffy', 
            bio: 'some guy from NJ',
            createdAt: 10000002
        })
        """
    )

    ids = get_incomplete_profile_ids()

    assert ids is not None
    assert ids == []


def test_incomplete_profiles_some_outputs():
    """
    get id of the case of some profiles are missing
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.gds.run_cypher(
        """
        MERGE (:TwitterAccount {
            userId: '111',
            createdAt: 10000000
        })
        MERGE (:TwitterAccount {
            userId: '112',
            createdAt: 10000001
        })
        MERGE (:TwitterAccount {
            userId: '113', 
            userName: 'Tuffy', 
            bio: 'some guy from NJ',
            createdAt: 10000002
        })
        """
    )

    ids = get_incomplete_profile_ids()

    assert ids == ["111", "112"]


def test_incomplete_profiles_by_bio_some_outputs():
    """
    get id of the case of some profiles are missing
    we have changed the `by` parameter so to see if it is working right
    """
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.gds.run_cypher(
        """
        MERGE (:TwitterAccount {
            userId: '111'
        })
        MERGE (:TwitterAccount {
            userId: '112'
        })
        MERGE (:TwitterAccount {
            userId: '113', 
            userName: 'Tuffy', 
            createdAt: 10000002
        })
        """
    )

    ids = get_incomplete_profile_ids(by="bio")

    assert ids == ["111", "112", "113"]
