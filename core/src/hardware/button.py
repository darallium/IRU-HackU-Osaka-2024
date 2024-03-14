import gpiod

class Button:
    def __init__(self, GPIO_SW):
        self.chip = gpiod.Chip("gpiochip4")
        self.sw=self.chip.get_line(GPIO_SW)
        self.sw.request(consumer="Button", type=gpiod.LINE_REQ_EV_RISING_EDGE, flags=8)

    def is_pushed(self):
        ev_lines = self.sw.event_wait(sec=0)
        if ev_lines:
            event = self.sw.event_read()
            return True
        else:
            return False
