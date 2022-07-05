import json
from box import Box


def read_json(file_path):
    """Reads a json file and returns a dictionary

    :param file_path: Path to the json file
    :return: Returns a dictionary with the json file content
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found: {}".format(file_path))
        return None
    except json.JSONDecodeError:
        print("Invalid JSON: {}".format(file_path))
        return None
    except Exception as e:
        print("{}".format(e))
        return None


class Settings:
    """
    Class for holding the application wide settings.
    """
    def __init__(self, file_path):
        self.config = self.get_settings(file_path)

    @staticmethod
    def get_settings(file_path):
        """Reads the settings from the JSON file.

        :param file_path: Path to the JSON file.
        :return: Box object containing the settings.
        """
        settings = read_json(file_path)
        if settings is None:
            print("No settings file found.")
            raise FileNotFoundError
        config = Box(settings)
        return config
