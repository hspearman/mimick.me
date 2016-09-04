import re


class FormatUtil:

    # Constants
    SENTENCE_REGEX = r"([^.?!]+[.!?]+[ ]*)"
    ENDING_PUNCTUATION = [".", "?", "!"]

    """ Returns a copy of a string with every sentence capitalized """
    @staticmethod
    def capitalize_sentences(text):

        # Split text into sentences
        sentences = re.findall(
            FormatUtil.SENTENCE_REGEX,
            text)

        # Loop through sentences
        for i in range(len(sentences)):

            # Capitalize first letter of sentence
            sentence = sentences[i]
            sentence = sentence[0].upper() + sentence[1:]
            sentences[i] = sentence

        # Re-combine sentences into one contiguous string
        text = "".join(sentences)

        return text

    """ Checks whether or not the string ends with a punctuation mark """
    @staticmethod
    def does_end_with_punctuation(text):
        return text[-1] in FormatUtil.ENDING_PUNCTUATION
