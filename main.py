from parsers.ParserFactory import ParserFactory
from sources.SourceFactory import SourceFactory
from util.FileUtil import FileUtil


def main():

    # Init variables
    source = SourceFactory.get_source()
    parser = ParserFactory.get_parser()

    # Load config data
    username = FileUtil.load_config(parser)

    # Get posts by username from source
    posts = source.get_user_posts(username)

    # Print generated string that mimics user's speech
    str_mimic = parser.mimic_user(posts)
    print(str_mimic)

main()


