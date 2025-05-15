import RPi.GPIO as GPIO
import time

class HWControl:
    def __init__(self, cfg):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.doors = cfg.doors
        # Set relays as outputs (LOW = locked), buttons as inputs with pull‑up
        for d in self.doors:
            GPIO.setup(d.relay_pin,  GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(d.button_pin, GPIO.IN,  pull_up_down=GPIO.PUD_UP)

    def unlock(self, door_idx, pulse_ms):
        """
        Energize the given door's relay for pulse_ms milliseconds.
        """
        pin = self.doors[door_idx].relay_pin
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(pulse_ms / 1000.0)
        GPIO.output(pin, GPIO.LOW)

    def is_button_pressed(self, door_idx):
        """
        Returns True if that door's learn‑button is pressed (active‑low).
        """
        pin = self.doors[door_idx].button_pin
        return GPIO.input(pin) == GPIO.LOW

    def cleanup(self):
        GPIO.cleanup()
