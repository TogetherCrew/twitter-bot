from .base_analytics import BaseAnalytics


class SimpleAnalytics(BaseAnalytics):
    def __init__(self, user_id: str) -> None:
        super().__init__(user_id)

    def get_account_overview(self, user_id: str) -> tuple[int, int]:
        """
        get the account overview analytics.
        the analytics are:
        1. Number of Accounts that engage with you
        2. Number of followers

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        ---------
        engagement_acc_count : int
            analytics 1
        follower_count : int
            analytics 2
        """
        result_engagement_count = self.gds.run_cypher(
            f"""
            OPTIONAL MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:QUOTED|REPLIED|RETWEETED]-(m:Tweet)
            WHERE m.authorId <> t.authorId AND r.createdAt >= {self.Epoch7daysAgo}
            WITH COLLECT(DISTINCT m.authorId) as interaction_authors

            OPTIONAL MATCH (a:TwitterAccount {{userId: '{user_id}'}}) <-[r:MENTIONED]-(t:Tweet)
            WHERE t.authorId <> a.userId AND r.createdAt >= {self.Epoch7daysAgo}
            WITH COLLECT(DISTINCT t.authorId) as mention_authors, interaction_authors

            OPTIONAL MATCH (t:Tweet {{authorId: '{user_id}'}}) <-[r:LIKED]-(a:TwitterAccount)
            WHERE t.authorId <> a.userId AND t.createdAt >= {self.Epoch7daysAgo}
            WITH COLLECT(DISTINCT a.userId) as liked_authors, mention_authors, interaction_authors

            WITH liked_authors + interaction_authors + mention_authors as people_list
            UNWIND people_list as people
            RETURN COUNT( DISTINCT people) as account_count
            """
        )
        engagement_acc_count = result_engagement_count["account_count"].iloc[0]

        result_follower_count = self.gds.run_cypher(
            f"""
            MATCH (a:TwitterAccount {{userId: '{user_id}'}})
            RETURN a.followerCount as followerCount
            """
        )
        follower_count = result_follower_count["followerCount"].iloc[0]
        return engagement_acc_count, follower_count

    def get_audience_response(self, user_id: str) -> tuple[int, int, int, int]:
        """
        get the audience response analytics. The analytics list are
        1. Number of replies others made on the user's posts
        2. Number of retweets others made on the user's posts
        3. Number of likes others made on the user's posts
        4. Number of Mentions

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Results
        --------
        replies_count : int
            analytics item 1
        retweets_count : int
            analytics item 2
        likes_count : int
            analytics item 3
        mentions_count : int
            analytics item 4
        """
        result_replies_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} )<-[r:REPLIED]-(m:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND m.authorId <> t.authorId
            RETURN COUNT(r) as reply_count
            """
        )
        replies_count = result_replies_count["reply_count"].iloc[0]

        result_retweets_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} )<-[r:RETWEETED]-(m:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND m.authorId <> t.authorId
            RETURN COUNT(r) as retweet_count
            """
        )
        retweets_count = result_retweets_count["retweet_count"].iloc[0]

        result_likes_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} ) <-[r:LIKED]- (a:TwitterAccount)
            WHERE t.createdAt >= {self.Epoch7daysAgo} AND a.userId <> t.authorId
            RETURN COUNT(r) as like_counts
            """
        )
        likes_count = result_likes_count["like_counts"].iloc[0]

        result_mentions_count = self.gds.run_cypher(
            f"""
            MATCH (a:TwitterAccount  {{userId: '{user_id}'}} )<-[r:MENTIONED]-(t:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND a.userId <> t.authorId
            RETURN COUNT(r) as mention_count
            """
        )
        mentions_count = result_mentions_count["mention_count"].iloc[0]

        return (replies_count, retweets_count, likes_count, mentions_count)

    def get_user_account_activity(self, user_id: str) -> tuple:
        """
        get the user account activity analytics. The list of analytics are
        1. Number of tweets the user made
        2. Number of replies the user made
        3. Number of retweets the user made
        4. *Number of likes the user made
        5. Number of mentions the user made

        * Not possible to compute accurately with the current twitter api

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Results
        --------
        tweet_count : int
            analytics item 1
        reply_count : int
            analytics item 2
        retweet_count : int
            analytics item 3
        mention_count : int
            analytics item 5
        """

        result_tweet_count = self.gds.run_cypher(
            f"""
            MATCH (a:TwitterAccount  {{userId: '{user_id}'}} )-[r:TWEETED]->(t:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo}
            RETURN COUNT(r) as tweet_count
            """
        )
        tweet_count = result_tweet_count["tweet_count"].iloc[0]

        result_reply_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} )-[r:REPLIED]->(m:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND m.authorId <> t.authorId
            RETURN COUNT(r) as reply_count
            """
        )
        reply_count = result_reply_count["reply_count"].iloc[0]

        result_retweet_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} )-[r:RETWEETED]->(m:Tweet)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND m.authorId <> t.authorId
            RETURN COUNT(r) as retweet_count
            """
        )
        retweet_count = result_retweet_count["retweet_count"].iloc[0]

        # result_like_counts = self.gds.run_cypher(
        #     f"""
        #     MATCH (a:TwitterAccount  {{userId: '{user_id}'}} )-[r:LIKED]->(m:Tweet)
        #     WHERE m.createdAt >= {self.Epoch7daysAgo} AND a.userId <> m.authorId
        #     RETURN COUNT(r) as like_counts
        #     """
        # )
        # like_counts = result_like_counts["like_counts"].iloc[0]

        result_mention_count = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet  {{authorId: '{user_id}'}} )-[r:MENTIONED]->(a:TwitterAccount)
            WHERE r.createdAt >= {self.Epoch7daysAgo} AND t.authorId <> a.userId
            RETURN COUNT(r) as mention_count
            """
        )
        mention_count = result_mention_count["mention_count"].iloc[0]

        return (tweet_count, reply_count, retweet_count, mention_count)
