from datetime import datetime, timedelta, timezone

from bot.db.neo4j_connection import Neo4jConnection


class BaseAnalytics:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        neo4j_connection = Neo4jConnection()
        self.gds = neo4j_connection.neo4j_ops.gds
        self.Epoch7daysAgo = int(
            (datetime.now(tz=timezone.utc) - timedelta(days=7)).timestamp()
        )
