import json
import sys

CONFIG_FILE_NAME = "config.json"
RESOURCES_DIRECTORY = "resources"
FILE_PATH_TEMPLATE = "./{0}/{1}"


class FileUtil:

    @staticmethod
    def load_config(parser):

        # Load config data from file
        config = FileUtil.get_resources_json_file(CONFIG_FILE_NAME)

        try:

            # Init username
            username = config["username"]

            # Configure parser
            parser.configure(
                config["token_group_size"],
                config["min_mimicked_text_length"],
                config["max_mimicked_text_length"])

        except KeyError:
            print("Failed to load config!")
            sys.exit()

        return username

    @staticmethod
    def get_resources_json_file(filename):

        # Format file path
        file_path = FILE_PATH_TEMPLATE.format(
            RESOURCES_DIRECTORY,
            filename)

        # Grab file at path
        data = FileUtil.get_data_from_file(file_path)

        try:

            # Deserialize file contents via JSON
            return json.loads(data)

        except ValueError:
            print("Failed to decode JSON!")
            sys.exit()

    @staticmethod
    def get_data_from_file(path):

        try:

            # Read contents of file
            with open(path, encoding='utf-8') as data_file:
                return data_file.read()

        except (IOError, FileNotFoundError):

            print("Failed to open file!")
            sys.exit()
