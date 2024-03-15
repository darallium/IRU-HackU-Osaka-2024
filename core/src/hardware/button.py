import subprocess
import time
import os
import select
import signal

class Button:
    def __init__(self, offset) -> None:
        self.offset = str(offset)
        temp = subprocess.Popen(["gpiomon", "-B", "pull-up", "gpiochip4", "18"])
        temp.send_signal(signal.SIGINT)

    def has_pushed(self):
        process = subprocess.Popen(['pinctrl', "get", self.offset], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if b' hi ' in stdout:
            return True
        elif b' lo ' in stdout:
            return False
        else:
            return True #ugokuka kowaikara torenakattara True