from abc import ABCMeta, abstractmethod


class ISource(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self): pass

    """

    Retrieves a user by {username} from source,
    and returns an array of user's most recent posts

    """
    @abstractmethod
    def get_user_posts(
            self,
            username): raise NotImplementedError
