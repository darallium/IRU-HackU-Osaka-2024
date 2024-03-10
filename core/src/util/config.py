import json
import os
import threading
import time
import util.logger as logger
from util.default_config import default_config
from util.default_config_linux import default_config_linux
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
        self.default_config_linux = default_config_linux
        self.load_config()
        self.last_modified = os.path.getmtime(self.config_file)
        self.check_config_updates()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            self.validate_config()
        else:
            logger.warning("Config file not found. Using default config.")
            if os.name == 'nt':
                self.config = self.default_config
            else:
                self.config = {**self.default_config, **self.default_config_linux}

            self.save_config()

    def validate_config(self):
        for key, value in self.default_config.items():
            if key not in self.config or type(self.config[key]) != type(value):
                logger.warning(f"Invalid config key: {key}. Using default value ;)")
                self.config[key] = value
        self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def check_config_updates(self):
        def target():
            while True:
                time.sleep(1)
                if os.path.getmtime(self.config_file) != self.last_modified:
                    logger.info("Config file updated. Reloading...")
                    self.last_modified = os.path.getmtime(self.config_file)
                    self.load_config()

        thread = threading.Thread(target=target)
        thread.start()

config = Config()


def value_of(key):
    return config.config[key]
    #config.config.get(key, default_value) にすればデフォルト値を返すようになる