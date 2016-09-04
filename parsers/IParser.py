from abc import ABCMeta, abstractmethod


class IParser(metaclass=ABCMeta):

    _token_group_size = -1
    _min_mimicked_text_length = -1
    _max_mimicked_text_length = -1

    @abstractmethod
    def __init__(self): pass

    """ Parses a user's posts, and returns a string that mimics their speech """
    @abstractmethod
    def mimic_user(
            self,
            posts): raise NotImplementedError

    def configure(
            self,
            token_group_size,
            min_mimicked_text_length,
            max_mimicked_text_length):

        global _token_group_size, \
            _min_mimicked_text_length,\
            _max_mimicked_text_length

        self._token_group_size = token_group_size
        self._min_mimicked_text_length = min_mimicked_text_length
        self._max_mimicked_text_length = max_mimicked_text_length

