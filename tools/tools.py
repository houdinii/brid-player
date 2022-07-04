import json
from box import Box


def read_json(file_path):
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
    def __init__(self, file_path):
        self.config = self.get_settings(file_path)

    @staticmethod
    def get_settings(file_path):
        settings = read_json(file_path)
        if settings is None:
            print("No settings file found.")
            raise FileNotFoundError
        config = Box(settings)
        return config
