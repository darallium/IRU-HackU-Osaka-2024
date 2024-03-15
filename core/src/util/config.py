import json
import os
import threading
import time
from util.default_config import default_config, valid_values
from util.default_config_linux import default_config_linux
class Config:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = {}
        self.valid_values = valid_values
        if os.name == 'nt':
            self.default_config = default_config
        else:
            self.default_config = {**default_config, **default_config_linux}
        self.load_config()
        self.last_modified = os.path.getmtime(self.config_file)
        self.check_config_updates()

    def __del__(self):
        self.stop_thread = True
        self.thread.join()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
            self.validate_config()
        else:
            print("Config file not found. Using default config.")
            self.config = self.default_config
            self.save_config()

    def validate_config(self):
        is_valid = True
        for key, value in self.default_config.items():
            if key not in self.config or type(self.config[key]) != type(value):
                print(f"Invalid config key: {key}. Using default value ;)")
                self.config[key] = value
                is_valid = False
            elif key in self.valid_values and self.config[key] not in self.valid_values[key]:
                print(f"Invalid value for {key}: {self.config[key]}. Using default value ;)")
                self.config[key] = value
                is_valid = False
        if not is_valid:
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def check_config_updates(self):
        def target():
            while not self.stop_thread:
                time.sleep(1)
                if os.path.getmtime(self.config_file) != self.last_modified:
                    print("Config file updated. Reloading...")
                    self.last_modified = os.path.getmtime(self.config_file)
                    self.load_config()

        self.stop_thread = False
        self.thread = threading.Thread(target=target, daemon=True)
        self.thread.start()

config = Config()

def value_of(key):
    return config.config[key]
    #config.config.get(key, default_value) にすればデフォルト値を返すようになる

def release():
    config.__del__()
