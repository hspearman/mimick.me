import praw

from sources.ISource import ISource

# Constants
COMMENT_LIMIT = 1000
USER_AGENT = "mimick.me 0.1"


class RedditSource(ISource):
    # region _reddit_api property

    @property
    def _reddit_api(self):
        return self.__reddit_api

    @_reddit_api.setter
    def _reddit_api(
            self,
            value):
        self.__reddit_api = value

    # endregion

    def __init__(self):
        super().__init__()

        # Initialize connection to reddit API
        self._reddit_api = praw.Reddit(user_agent=USER_AGENT)

    def get_user_posts(
            self,
            username):

        assert (username is not None and username is not "")

        # Get reddit user
        user = self._reddit_api.get_redditor(username)

        # Collect {COMMENT_LIMIT} of user's most recent comments
        comments = []
        for comment in user.get_comments(limit=COMMENT_LIMIT):
            comments.append(comment.body)

        return comments
