import random
from parsers.IParser import IParser
from util.FormatUtil import FormatUtil


class Parser(IParser):

    def __init__(self):
        pass

    def mimic_user(
            self,
            posts):

        # Generate token groups from all of user's posts
        total_token_groups = self._tokenize_posts(posts)

        # Generate speech dictionary based on token groups
        speech_dictionary = self._generate_speech_dictionary(total_token_groups)

        # Generate mimicked text based on speech dictionary
        mimicked_text = self._generate_mimicked_text(speech_dictionary)

        # Format mimicked text
        mimicked_text_formatted = self._format_generated_text(mimicked_text)

        return mimicked_text_formatted

    """ Accumulates a master list of token groups from user's posts """
    def _tokenize_posts(
            self,
            posts):

        # Loop through posts ...
        total_token_groups = []
        for post in posts:

            # Tokenize post into groups
            token_groups = self._tokenize(post)

            # Skip invalid token groups
            if token_groups is None:
                continue

            # Add token groups to running total
            total_token_groups += token_groups

        return total_token_groups

    """

    Tokenizes a string into multiple token groups of size {TOKEN_GROUP_SIZE}.
    NOTE: Token groups are overlapping!

    Example:

    Let:
        text = "The quick brown fox jumps over the lazy dog"
        TOKEN_GROUP_SIZE = 3
    Result:
    [
        ["The", "quick", "brown"],
        ["quick", "brown", "fox"],
        ...
        ["the", "lazy, "dog"]
    ]

    """
    def _tokenize(
            self,
            text):

        # Split text into array of individual words
        words = text.split()

        # If text too short to tokenize ...
        num_of_words = len(words)
        if num_of_words < self._token_group_size:

            # Early-out
            return

        # Calculate start index of last possible token group
        # (otherwise, we'll "fall-off" end of array without enough tokens to fill last group!)
        index_of_last_token_group = self._token_group_size - 1

        # Iterate through words to generate token groups
        token_groups = []
        for pos in range(num_of_words - index_of_last_token_group):

            # Generate token group that starts from current position
            token_group = []
            for token_pos in range(
                    pos,
                    pos + self._token_group_size):

                token_group.append(words[token_pos])

            # Record token group
            token_groups.append(token_group)

        return token_groups

    """ Generates a speech dictionary for user based on token groups parsed from posts """
    def _generate_speech_dictionary(
            self,
            total_token_groups):

        speech_dictionary = {}

        # Loop through token groups ...
        for token_group in total_token_groups:

            # Add (or update existing) entry in speech dictionary for token group
            self._add_or_update_speech_dictionary_entry(
                token_group,
                speech_dictionary)

        return speech_dictionary

    """

    Adds or updates a dictionary entry for token group in speech dictionary.

    Let:
        token_group = ["the", "quick", "brown"]
        TOKEN_GROUP_SIZE = 3

    Result:
        key = ["the", "quick"]
        value = ["brown"]

    """
    @staticmethod
    def _add_or_update_speech_dictionary_entry(
            token_group,
            speech_dictionary):

        # Create key for dictionary entry
        # (i.e. use all but last word!)
        key = tuple(token_group[0:-1])

        # Grab last token as value
        # (enclose it within array)
        value = [token_group[-1]]

        # Add (or update existing) entry in speech dictionary
        speech_dictionary[key] = value \
            if key not in speech_dictionary \
            else speech_dictionary[key] + value

    """

    Given a speech dictionary, generates text of {MIMICKED_TEXT_LENGTH} that mimick's users speech.

    """
    def _generate_mimicked_text(
            self,
            speech_dictionary):

        mimicked_text = ""

        # While mimicked text has not satisfied a stopping condition yet ...
        #
        # Stopping conditions:
        # - Mimicked text reached maximum length
        # - Mimicked text reached minimum length and ends with punctuation
        is_max_length_reached = False
        is_min_length_reached = False
        does_end_with_punctuation = False
        while not is_max_length_reached \
                and not (is_min_length_reached and does_end_with_punctuation):

            # If sequence follows another ...
            is_first_sequence = len(mimicked_text) == 0
            if not is_first_sequence:

                # Separate from previous sequence with a space
                mimicked_text += " "

            # Generate a sequence of mimicked text
            mimicked_text = self._generate_mimicked_sequence(
                speech_dictionary,
                mimicked_text)

            # Check if word count is within length constraints
            word_count = len(mimicked_text.split())
            is_min_length_reached = word_count >= self._min_mimicked_text_length
            is_max_length_reached = word_count >= self._max_mimicked_text_length

            # Check if punctuation correct
            does_end_with_punctuation = FormatUtil.does_end_with_punctuation(mimicked_text)

        return mimicked_text

    """

    Given a speech dictionary and pre-existing text, appends a generated sequence to pre-existing text
    that mimics a user's speech.

    A sequence ends when either:
        - Maximum text length of {MIMICKED_TEXT_LENGTH} is reached
        - No options exist for next word (i.e. hit a dead end)

    """
    def _generate_mimicked_sequence(
            self,
            speech_dictionary,
            mimicked_text):

        # Append random start key to pre-existing text
        mimicked_text, random_start_key = self._append_random_start_key(
            speech_dictionary,
            mimicked_text)

        # Track key used for generation of next word
        current_key = random_start_key

        # Track word count of running text
        word_count = len(mimicked_text.split())

        # While mimicked text has not reached desired length yet
        # and next key exists in speech dictionary ...
        is_key_existent = True
        is_length_reached = False
        while not is_length_reached \
                and is_key_existent:

            # Generate next word with current key
            current_key, next_word = self._generates_next_word(
                current_key,
                speech_dictionary)

            # Append next word to running text
            mimicked_text += str.format(
                " {0}",
                next_word)

            # Update word count
            word_count += 1
            is_length_reached = word_count >= self._min_mimicked_text_length

            # Check if key exists
            is_key_existent = current_key in speech_dictionary

        return mimicked_text

    """

    Given a key, generates the next word in a sequences of mimicked text.
    NOTE: The next word is randomly selected from the word pool associated with given key.

    Example:

    Let:
        key = ["the, "quick"]
        speech_dictionary = [
            ["the", "quick"] : ["brown", "rabbit"]
        ]

    Result:
        next_word = "rabbit"

    """
    @staticmethod
    def _generates_next_word(
            key,
            speech_dictionary):

        # Get pool of possible words (based on key)
        word_pool = speech_dictionary[key]

        # Pick random word from pool
        random_word = random.choice(word_pool)

        # Generate next key based on resulting random word
        #
        # Example:
        #
        # Let:
        #   key = ("the", "quick")
        #   random_word = "brown"
        #
        # Result:
        #   next_key = ("quick", "brown")
        next_key = key[1:]
        next_key += tuple([random_word])

        return next_key, random_word

    """ Formats the mimicked text to use correct capitalization, etc. """
    @staticmethod
    def _format_generated_text(mimicked_text):

        # If mimicked text does not end with punctuation ...
        if not FormatUtil.does_end_with_punctuation(mimicked_text):

            # Add random punctuation mark to end
            mimicked_text += str.format(random.choice(FormatUtil.ENDING_PUNCTUATION))

        # Capitalize all sentences in mimicked text
        mimicked_text = FormatUtil.capitalize_sentences(mimicked_text)

        return mimicked_text

    """ Selects a random key from the given speech dictionary, then appends it to the mimicked text string. """
    @staticmethod
    def _append_random_start_key(
            speech_dictionary,
            mimicked_text):

        # Get random key from speech dictionary
        keys = list(speech_dictionary.keys())
        random_start_key = random.choice(keys)

        # Append as starting text
        random_start_text = " ".join(random_start_key)
        mimicked_text += random_start_text

        return mimicked_text, random_start_key
