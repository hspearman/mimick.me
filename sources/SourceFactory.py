from sources.RedditSource import RedditSource


class SourceFactory:

    @staticmethod
    def get_source():
        return RedditSource()
