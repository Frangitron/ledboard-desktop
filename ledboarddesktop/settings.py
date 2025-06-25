import os
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    firmware_filepath: str = ""

    def load(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                content = f.read()
                loaded_settings = Settings.from_json(content)
                self.__dict__.update(loaded_settings.__dict__)

    def save(self):
        with open("settings.json", "w") as f:
            f.write(self.to_json(indent=2))
