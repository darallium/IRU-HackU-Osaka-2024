import json
import os
import src.util.logger as logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


# FileSystemEventHandlerを継承したクラス
class ConfigHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def on_modified(self, event):
        self.config.reload_config()
        threading.Thread(target=self.config.watch_config).start()


class Config:
    _instance = None

    # シングルトン
    def __new__(cls, path="config.json"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, path="config.json"):
        self.path = path
        self.config = {}
        self.event_handler = None
        self.load_config()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, os.path.dirname(self.path))
        self.observer.start()

    def load_config(self):
        self.config = {}
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config = json.load(f)
        else:
            logger.error("Config file not found")

        self.event_handler = ConfigHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, os.path.dirname(self.path))
        self.observer.start()

    def write_config(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get_value(self, key, ifnull):
        if self.is_file_changed():
            self.load_config()
        if key in self.config:
            return self.config[key]
        else:
            return ifnull

    def set_value(self, key, value):
        if self.is_file_changed():
            self.load_config()
        self.config[key] = value
        self.write_config()

    def watch_config(self):
        self.observer.stop()
        self.observer.join()

    def stop_watch(self):
        self.observer.stop()
        self.observer.join()

    def is_file_changed(self):
        return self.observer.event_queue is not None


