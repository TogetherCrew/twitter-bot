import pandas as pd

from .base_analytics import BaseAnalytics


class AdvancedAnalytics(BaseAnalytics):
    def __init__(self, user_id: str) -> None:
        super().__init__(user_id)

    def get_engagement_by_account_counts(
        self, user_id: str
    ) -> tuple[int, int, int, int]:
        """
        get the count of users for engagement by account analytics. the analytics are
        1. High quality and low amount
        2. High quality and high engagement
        3. Low quality and low amount
        4. Low quality and high engagement

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        analytics_1 : int
            the accounts related to first item of analytics
        analytics_2 : int
            the accounts related to second item of analytics
        analytics_3 : int
            the accounts related to third item of analytics
        analytics_4 : int
            the accounts related to fourth item of analytics
        """

        (
            analytics_1,
            analytics_2,
            analytics_3,
            analytics_4,
        ) = self.get_engagement_by_account_users(user_id)

        return (
            len(analytics_1),
            len(analytics_2),
            len(analytics_3),
            len(analytics_4),
        )

    def get_engagement_by_account_users(
        self, user_id: str
    ) -> tuple[list[str], list[str], list[str], list[str]]:
        """
        find the users for each activity type
        1. High quality and low amount
        2. High quality and high engagement
        3. Low quality and low amount
        4. Low quality and high engagement

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        analytics_1 : list[str]
            the accounts related to first item of analytics
        analytics_2 : list[str]
            the accounts related to second item of analytics
        analytics_3 : list[str]
            the accounts related to third item of analytics
        analytics_4 : list[str]
            the accounts related to fourth item of analytics
        """
        df_replies = self.get_user_reply_count(user_id)
        df_quotes = self.get_user_quote_count(user_id)
        df_mention = self.get_user_mention_count(user_id)
        df_retweet = self.get_user_retweet_count(user_id)
        df_likes = self.get_user_likes_count(user_id)

        merged_df = pd.merge(df_replies, df_quotes, on="user", how="outer")
        merged_df = pd.merge(merged_df, df_mention, on="user", how="outer")
        merged_df = pd.merge(merged_df, df_retweet, on="user", how="outer")
        merged_df = pd.merge(merged_df, df_likes, on="user", how="outer")
        merged_df = merged_df.fillna(0)

        # extracting users for each analytics
        df_temp = merged_df[merged_df["reply_count"] < 3]
        df_temp = df_temp[df_temp["quote_count"] < 3]
        df_temp = df_temp[df_temp["mention_count"] < 3]
        analytics_1 = list(df_temp["user"].values)

        df_temp = merged_df[merged_df["reply_count"] > 2]
        df_temp = df_temp[df_temp["quote_count"] > 2]
        df_temp = df_temp[df_temp["mention_count"] > 2]
        analytics_2 = list(df_temp["user"].values)

        df_temp = merged_df[merged_df["retweet_count"] < 3]
        df_temp = df_temp[df_temp["likes_count"] < 3]
        analytics_3 = list(df_temp["user"].values)

        df_temp = merged_df[merged_df["retweet_count"] > 2]
        df_temp = df_temp[df_temp["likes_count"] > 2]
        analytics_4 = list(df_temp["user"].values)

        return analytics_1, analytics_2, analytics_3, analytics_4

    def get_user_reply_count(self, user_id: str) -> pd.DataFrame:
        """
        Get reply count of each user on the user_id's tweets

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        reply_count_per_acc : pd.DataFrame
            the reply count per twitter account
        """
        reply_count_per_acc = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:REPLIED]-(m:Tweet)
            WHERE m.authorId <> t.authorId AND r.createdAt >= {self.Epoch7daysAgo}
            RETURN m.authorId AS user, COUNT(*) as reply_count
            """
        )
        return reply_count_per_acc

    def get_user_quote_count(self, user_id: str) -> pd.DataFrame:
        """
        Get quote count of each user on the user_id's tweets

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        quote_count_per_acc : pd.DataFrame
            the quote count per twitter account
        """
        quote_count_per_acc = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:QUOTED]-(m:Tweet)
            WHERE m.authorId <> t.authorId AND r.createdAt >= {self.Epoch7daysAgo}
            RETURN m.authorId AS user, COUNT(*) as quote_count
            """
        )
        return quote_count_per_acc

    def get_user_mention_count(self, user_id: str) -> pd.DataFrame:
        """
        Get mention count of each user on the user_id's tweets

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        mention_count_per_acc : pd.DataFrame
            the mention count per twitter account
        """
        mention_count_per_acc = self.gds.run_cypher(
            f"""
            MATCH (a:TwitterAccount {{userId: '{user_id}'}})<-[r:MENTIONED]-(t:Tweet)
            WHERE a.userId <> t.authorId AND r.createdAt >= {self.Epoch7daysAgo}
            RETURN t.authorId AS user, COUNT (*) as mention_count
            """
        )
        return mention_count_per_acc

    def get_user_retweet_count(self, user_id: str) -> pd.DataFrame:
        """
        Get retweet count of each user on the user_id's tweets

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        retweet_count_per_acc : pd.DataFrame
            the retweet count per twitter account
        """
        retweet_count_per_acc = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet {{authorId: '{user_id}'}})<-[r:RETWEETED]-(m:Tweet)
            WHERE t.authorId <> m.authorId AND r.createdAt >= {self.Epoch7daysAgo}
            RETURN m.authorId AS user, COUNT (*) as retweet_count
            """
        )
        return retweet_count_per_acc

    def get_user_likes_count(self, user_id: str) -> pd.DataFrame:
        """
        Get likes count of each user on the user_id's tweets

        Parameters
        -----------
        user_id : str
            the user id we would use to obtain results

        Returns
        --------
        likes_count_per_acc : pd.DataFrame
            the likes count per twitter account
        """
        likes_count_per_acc = self.gds.run_cypher(
            f"""
            MATCH (t:Tweet {{authorId: '{user_id}'}}) <-[:LIKED]- (a:TwitterAccount)
            WHERE a.userId <> t.authorId
            RETURN a.userId as user, COUNT(*) as likes_count
            """
        )
        return likes_count_per_acc
