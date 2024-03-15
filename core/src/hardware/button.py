import subprocess
import time
import os
import select
import signal

class Button:
    def __init__(self, offset) -> None:
        self.offset = str(offset)

    def has_pushed(self):
        process = subprocess.Popen(['pinctrl', "get", self.offset], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if b' hi ' in stdout:
            return True
        elif b' lo ' in stdout:
            return False
        else:
            return None