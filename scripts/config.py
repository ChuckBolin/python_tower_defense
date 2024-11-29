import os
import yaml

class Config:
    def __init__(self, config_file="config.yaml"):
        """
        Initialize the Config class and load the configuration file.
        If the file is missing or incomplete, default values are used.
        """
        self.default_values = {
            "game_info": {
                "game_title": "Standard Program",
                "game_version": 0.1,
                "game_dev_date": "November 2024",
                "screen_width": 800,
                "screen_height": 600,
                "fps": 60,
            }
        }
        self.config = self.load_config(config_file)
        self.initialize_class_variables()

    def load_config(self, config_file):
        """
        Load the configuration file. If it's missing or incomplete,
        merge with default values.
        """
        if not os.path.exists(config_file):
            print(f"Config file '{config_file}' not found. Using default values.")
            return self.default_values

        try:
            with open(config_file, "r") as file:
                config_data = yaml.safe_load(file)
                return self.merge_defaults(config_data)
        except (yaml.YAMLError, IOError) as e:
            print(f"Error reading config file: {e}. Using default values.")
            return self.default_values

    def merge_defaults(self, config_data):
        """
        Merge loaded config data with default values, ensuring missing keys
        are filled in.
        """
        merged_config = self.default_values.copy()
        for key, value in config_data.items():
            if key in merged_config and isinstance(value, dict):
                # Merge sub-dictionaries
                merged_config[key].update(value)
            else:
                merged_config[key] = value
        return merged_config

    def initialize_class_variables(self):
        """
        Initialize class variables from the loaded configuration.
        """
        game_info = self.config.get("game_info", {})
        self.game_title = game_info.get("game_title", self.default_values["game_info"]["game_title"])
        self.game_version = game_info.get("game_version", self.default_values["game_info"]["game_version"])
        self.game_dev_date = game_info.get("game_dev_date", self.default_values["game_info"]["game_dev_date"])
        self.screen_width = game_info.get("screen_width", self.default_values["game_info"]["screen_width"])
        self.screen_height = game_info.get("screen_height", self.default_values["game_info"]["screen_height"])
        self.fps = game_info.get("fps", self.default_values["game_info"]["fps"])

    def __repr__(self):
        """
        String representation for debugging purposes.
        """
        return (
            f"Config("
            f"game_title='{self.game_title}', "
            f"game_version={self.game_version}, "
            f"game_dev_date='{self.game_dev_date}', "
            f"screen_width={self.screen_width}, "
            f"screen_height={self.screen_height}, "
            f"fps={self.fps}"
            f")"
        )