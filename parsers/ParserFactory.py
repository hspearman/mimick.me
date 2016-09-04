from parsers.Parser import Parser


class ParserFactory:

    @staticmethod
    def get_parser():
        return Parser()
