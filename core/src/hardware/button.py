import gpiod

class Button:
    def __init__(self, GPIO_SW):
        self.chip = gpiod.Chip("gpiochip4")
        self.sw=self.chip.get_line(GPIO_SW)
        self.sw.request(consumer="Button", type=gpiod.LINE_REQ_EV_RISING_EDGE, flags=8)

    def is_pushed(self):
        return self.sw.event_poll(sec=0) is not None
