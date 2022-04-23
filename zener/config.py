import os
from configparser import ConfigParser


class Config:
    secret: str
    application_id: str
    command_mode: str

    def __init__(self, config_file="config.ini"):
        # Get the configparser object
        self.config_object = ConfigParser()

        # Set defaults.
        self.config_object["DISCORD"] = {
            "secret": "your_secret_token",
            "application_id": "your_your_application_id",
            "command_mode": "guild",  # guild or global
        }

        # Read current file if exists.
        if os.path.exists(config_file):
            self.config_object.read(config_file)

        # Write back to config file to save default config to file.
        with open(config_file, "w") as conf:
            self.config_object.write(conf)

        # Set this object's attributes to the config values.
        for section in self.config_object.sections():
            for key, value in self.config_object[section].items():
                setattr(self, key, value)
