import json
import os
import util.logger as logger
from util.default_config import default_config

class Config:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {}
        self.default_config = default_config
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            self.validate_config()
        else:
            self.config = self.default_config
            self.save_config()

    def validate_config(self):
        for key, value in self.default_config.items():
            if key not in self.config or type(self.config[key]) != type(value):
                logger.warning(f"Invalid config key: {key}. Using default value ;)")
                self.config[key] = value
        self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

config = Config()

def value_of(key):
    return config.config[key]
